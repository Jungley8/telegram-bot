from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp as youtube_dl
import re
import logging
import os
import requests
import shutil

# 设置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 支持的链接格式
patterns = {
    'twitter': r'https?://(www\.)?twitter\.com/\w+/status/\d+',
    'twitter_short': r'https?://t\.co/\S+',
    'x_twitter': r'https?://x\.com/\w+/status/\d+',
    'youtube': r'https?://(www\.)?youtube\.com/watch\?v=\S+|https?://youtu\.be/\S+'
}


def help_command(update: Update, context: CallbackContext) -> None:
    help_text = "Here are the commands you can use:\n"
    help_text += "/hello - Greet the user\n"
    help_text += "/youtube [link] - This command forces the bot to download the specified video.\n"
    help_text += "Send me a link, I will download the video or GIF for you.\n"
    # 添加更多帮助文本
    update.message.reply_text(help_text)


def start(update: Update, context: CallbackContext) -> None:
    promotion = os.getenv('TELEGRAM_START_PROMOTION')
    start_message = (
        f"Hello {update.effective_user.first_name}, 欢迎使用本机器人！\n\n"
        "使用说明：\n"
        "- 直接发送Twitter或YouTube链接，我将帮您下载视频。\n"
        "- TG单文件限制最大50M\n"
        "- 支持的链接格式包括 'twitter.com', 't.co', 和 'x.com' 域名下的Twitter链接，以及YouTube视频链接。\n"
        "- 只需发送链接即可，机器人会自动处理并回复相应的视频。\n\n"
        f"{promotion}"
        "如果遇到问题或有任何疑问，随时发送/help获取帮助。\n"
        "If you encounter any problems or have any questions, feel free to send /help to get assistance."
    )
    update.message.reply_text(start_message, parse_mode='Markdown', disable_web_page_preview=True)

def download_video(info_dict, url_type, user_id):
    ydl_opts = {
        'format': 'worst' if url_type == 'youtube' else 'best', # best[filesize<50M] 不支持
        # currently supported: avi, flv, gif, mkv, mov, mp4, webm, aac, aiff, alac, flac, m4a, mka, mp3, ogg, opus, vorbis, wav
        'nocheckcertificate': True,
        'outtmpl': f'downloads/{user_id}/%(id)s.%(ext)s',  # 保存文件的模板
        'quiet': True,
    }
    # 为每个用户创建一个唯一的目录
    user_dir = f'downloads/{user_id}'
    shutil.rmtree(user_dir)
    os.mkdir(user_dir)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([info_dict])

def identify_url_type(url):

    for url_type, pattern in patterns.items():
        if re.match(pattern, url):
            return url_type, re.search(pattern, url).group(0)

    return 'unknown', ''

def get_video_info(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict

# TODO 文件太大给出提示
def handle_download_request(url, type, user_id):
    info_dict = get_video_info(url)

    # 检查文件大小，单位为字节，50MB = 50 * 1024 * 1024
    video_filesize = info_dict.get('filesize') or 0
    if video_filesize <= 50 * 1024 * 1024:
        download_video(url, type, user_id)
        return info_dict
    else:
        return { 'error': '视频文件太大，无法下载（超过50MB）。\nVideo is too large to download (over 50MB).' }

def handle_link(update, message, force = False):
    user_id = update.message.from_user.id  # 获取用户的Telegram ID
    url_type, url = identify_url_type(message)

    if url_type != 'unknown':
        processMessage = update.message.reply_text(f'检测到链接，处理中……\nDetected a link, processing...')
        if url_type == 'x_twitter':
            url = url.replace("x.com", "twitter.com")

        try:
            if (url_type != 'youtube' or force == True):
                download_video(url, url_type, user_id)
                # info = handle_download_request(url, url_type, user_id)
                # # 文件太大
                # if info.get('error'):
                #     processMessage.edit_text(info.get('error'))
                #     return

                dir = f'downloads/{user_id}/'
                # 寻找最新下载的文件
                video_file = max([dir + f for f in os.listdir(dir)], key=os.path.getctime)
                # 回复用户视频
                try:
                    with open(video_file, 'rb') as video:
                        update.message.reply_video(video=video)
                        processMessage.delete() # remove processMessage
                except Exception as e:
                    logger.error(e)
                    processMessage.edit_text('无法回复视频。\nUnable to reply to the video.')

                os.remove(video_file)  # 删除文件以防止占用太多空间

            else:
                processMessage.edit_text("无需下载，可直接点击预览观看\n No need to download, you can preview and watch directly.")

        except Exception as e:
            logger.error(e)
            processMessage.edit_text('无法下载视频。\nError downloading the video.')
    else:
        update.message.reply_text('请发送有效链接\nPlease send a valid link.')


def handle_message(update, context):
    message = update.message.text
    handle_link(update, message)

def download_youtube(update, context):
    message = update.message.text
    if message.startswith('/youtube '):
        # 提取URL部分
        url = message.split(' ', 1)[1].strip()
        handle_link(update, url, True)
    else:
        update.message.reply_text('请发送有效链接\nPlease send a valid link.')

def main():
    # 从环境变量获取Token
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    if TOKEN is None:
        logger.error("No token provided. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    REQUEST_KWARGS={}
    PROXY_URL = os.getenv('PROXY_URL')
    if PROXY_URL is not None:
        # "USERNAME:PASSWORD@" is optional, if you need authentication:
        # 'proxy_url': 'http://192.168.101.13:7890',
        REQUEST_KWARGS['proxy_url'] = PROXY_URL

    # 使用run_polling()的try-except块以优雅地处理意外情况
    try:
        updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("youtube", download_youtube))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        updater.start_polling()
    except Exception as e:
        logger.error("Error in running bot: %s", str(e))

    updater.idle()

if __name__ == '__main__':
    main()

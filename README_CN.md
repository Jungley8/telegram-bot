# Twitter 和 YouTube 视频下载 Telegram 机器人

欢迎来到我们的 Telegram 机器人 GitHub 仓库。该机器人旨在通过 Telegram 简化从 Twitter 和 YouTube 下载视频的过程。本机器人用户友好、高效，并支持多种链接格式。

## 特点

- **轻松下载视频**：发送 Twitter 或 YouTube 链接，机器人将帮助您下载视频。
- **支持的链接格式**：包括 'twitter.com', 't.co', 和 'x.com' 域名下的 Twitter 链接，以及 YouTube 视频链接。
- **自动处理**：只需发送链接，机器人便会处理剩余部分，并回复相应的视频文件。
- **支持代理**：机器人现支持设置代理访问 Telegram API，确保在访问受限的地区也能顺畅运行。

## 使用方法

1. **启动机器人**：在 Telegram 上向机器人发送消息开始。
2. **发送链接**：粘贴您希望下载的 Twitter 或 YouTube 链接。
3. **接收视频**：机器人将处理链接并发送回视频文件。
4. **配置代理**：如果您所在的地区 Telegram 受到限制，您可以配置机器人使用代理，以实现不间断访问。

## 获取帮助

- 如遇任何问题或有疑问，可在机器人中使用 `/help` 命令获得协助。
- 您也可以参阅此 README 或在此 GitHub 仓库上发起问题以获取支持。

## 限制

- **文件大小限制**：Telegram 单文件限制最大为 50MB。

## 使用 Docker Compose 部署

本节说明如何使用 Docker Compose 部署 Telegram 机器人。

### 先决条件

- Docker
- Docker Compose
- [创建 Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot)

### 步骤

1. **克隆仓库**：将此仓库克隆到本地机器。

    ```bash
    git clone https://github.com/Jungley8/telegram-bot
    cd telegram-bot
    cp .env.example .env
    ```

2. **环境变量**：在项目根目录 `.env` 文件中，添加必要的环境变量。

    ```env
    PROXY_URL=您的代理网址
    TELEGRAM_TOKEN=您的Telegram机器人令牌
    ```
3. **构建并运行**：使用 Docker Compose 构建并运行容器。

    ```bash
    docker-compose up -d --build
    ```

4. **访问机器人**：您的 Telegram 机器人现在应该正在运行，并可以通过 Telegram 访问。


## 贡献

欢迎对机器人进行改进的贡献。请随意 Fork 本仓库，进行更改，并提交 Pull Request。

## 许可证

本项目为开源，适用的许可证为 MIT。

## 致谢

特别感谢所有贡献者和本机器人的用户，他们的持续支持和反馈至关重要。

---

**注意**：本机器人是社区驱动的项目，与 Twitter、YouTube 或 Telegram 无关。

---

祝您使用愉快，如有任何帮助或改进建议，请随时联系！

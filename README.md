# Telegram Bot for Twitter and YouTube Video Download

> [简体中文](./README_CN.md)

Welcome to the GitHub repository of our Telegram Bot designed to simplify the process of downloading videos from Twitter and YouTube directly through Telegram. This bot is user-friendly, efficient, and supports various link formats.

## Features

- **Download Videos Easily**: Send Twitter or YouTube links, and the bot will assist you in downloading the videos.
- **Supported Link Formats**: Includes links from 'twitter.com', 't.co', and 'x.com' domains for Twitter, as well as YouTube video links.
- **Automatic Processing**: Just send the link, and the bot will handle the rest, replying with the corresponding video.
- **Proxy Support**: The bot now supports setting up a proxy to access Telegram API, ensuring smooth operation even in regions where access might be restricted.


## Usage

1. **Start the Bot**: Begin by sending a message to the bot on Telegram.
2. **Send a Link**: Paste the Twitter or YouTube link you wish to download.
3. **Receive Your Video**: The bot will process the link and send back the video file.
4. **Configure Proxy**: If you are in a region where Telegram is restricted, you can configure the bot to use a proxy for uninterrupted access.

## Limits

- **File Size Limit**: Telegram's single file limit is a maximum of 50MB.


## Deployment with Docker Compose

This section explains how to deploy the Telegram Bot using Docker Compose.

### Prerequisites

- Docker
- Docker Compose
- [Create a Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot)

### Steps

1. **Clone the Repository**: Clone this repository to your local machine.

    ```bash
    git clone https://github.com/Jungley8/telegram-bot
    cd telegram-bot
    cp .env.example .env
    ```

2. **Environment Variables**: add the necessary environment variables to `.env` files.

    ```env
    PROXY_URL=your_proxy_url
    TELEGRAM_TOKEN=your_telegram_bot_token
    ```

3. **Build and Run**: Use Docker Compose to build and run the container.

    ```bash
    docker-compose up -d --build
    ```

4. **Access the Bot**: Your Telegram bot should now be running and accessible via Telegram.


## Getting Help

- If you encounter any issues or have questions, use the `/help` command in the bot to get assistance.
- You can also refer to this README or open an issue on this GitHub repository for support.

## Contributing

Contributions to improve the bot are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-source and available under MIT.

## Acknowledgments

A special thanks to all the contributors and users of this bot for their continuous support and feedback.

---

**Note:** This bot is a community-driven project and is not affiliated with Twitter, YouTube, or Telegram.

---

Enjoy using the bot, and don't hesitate to reach out for help or suggest improvements!

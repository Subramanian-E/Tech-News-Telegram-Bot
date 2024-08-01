# Tech News Telegram Bot 📰

A Python bot that scrapes the latest technology news and can be scheduled to create an image post, then send it to a Telegram channel.

## Installation ⚒️

To install and set up the bot, follow these steps:

```bash
git clone https://github.com/Subramanian-E/Tech-News-Telegram-Bot
cd Tech-News-Telegram-Bot
pip install -r requirements.txt
```

After installation, check the `config.yaml` file to configure your settings.

## Configuration

Open the `config.yaml` file and update the following settings with your own values:

- `telegram_bot_token`: Your Telegram bot token.
- `schedule_time`: The time at which the bot should post the news.
- `chat_id`: The Telegram chat ID where the news will be posted.
- `join_url`: The URL for the "Join Us" button.
- `font_path`: The path to the font file.
- `cover_image_path`: The path to the cover image file.

## Demo ✨
### Cover Image

Below is an example of the cover image that the bot will use:

<img src="https://github.com/user-attachments/assets/1e0617d4-4647-4ea9-a492-8f1ff692e799" alt="Cover" width="400"/>

### Post On Channel

Here is an example of a post that the bot will create and send to your Telegram channel:

![Post](https://github.com/user-attachments/assets/97846a72-82bd-41c1-a8ec-68069f2cf135)

## Usage
Run the bot using the following command:

```bash
python main.py
```

The bot will fetch the latest technology news from Inshorts, create an image post, and send it to the specified Telegram channel at the scheduled time.

Feel free to contribute to the project or report any issues you encounter.



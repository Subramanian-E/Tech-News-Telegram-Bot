import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap
import telegram
from telegram.ext import Updater
from pathlib import Path
import yaml
import re

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

TELEGRAM_BOT_TOKEN = config['telegram_bot_token']
SCHEDULE_TIME = config['schedule_time']
CHAT_ID = config['chat_id']
JOIN_URL = config['join_url']
FONT_PATH = config['font_path']
COVER_IMAGE_PATH = config['cover_image_path']
POST_IMAGE_PATH = 'Post.png'
THUMBNAIL_IMAGE_PATH = 'thumbnail.png'


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=30)
    for line in lines:
        line_width, line_height = font.getbbox(line)[-2:]
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height

def fetch_inshorts_news():
    url = "https://inshorts.com/en/read/technology"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    titles = [title.text for title in soup.find_all("span", itemprop="headline")]
    descriptions = [desc.text for desc in soup.find_all("div", itemprop="articleBody")]
    times = [time.text.split(',')[1].strip() for time in soup.find_all("span", class_="date")]
    images = [div['style'].split("url(")[1].split(")")[0].strip("'") for div in
              soup.find_all('div', style=lambda s: s and 'background-image' in s)]
    return titles, descriptions, times, images


def create_image(title, image_url):
    response = requests.get(image_url)
    image_path = Path(THUMBNAIL_IMAGE_PATH)
    with image_path.open("wb") as img_file:
        img_file.write(response.content)

    thumbnail = Image.open(image_path).convert("RGBA")
    square_thumbnail = crop_max_square(thumbnail)
    square_thumbnail.save(image_path, quality=95)

    resized_thumbnail = square_thumbnail.resize((500, 500))
    base_image = Image.open(COVER_IMAGE_PATH).convert("RGBA")
    base_image.paste(resized_thumbnail, (300, 300), resized_thumbnail)

    font = ImageFont.truetype(FONT_PATH, 55)
    draw_multiple_line_text(base_image, title, font, (8, 8, 8), 850)
    base_image.save(POST_IMAGE_PATH)


# Function to send the post to Telegram
def send_post(context):
    print("Started Posting")
    date_today = time.strftime("%d").zfill(2)
    titles, descriptions, times, images = fetch_inshorts_news()

    for i, post_date in enumerate(times):
        if re.sub(r'\D', '', post_date).zfill(2) == date_today:
            time.sleep(3)
            try:
                title = titles[i]
                description = descriptions[i]
                image_url = images[i]

                print(f"Title: {title}")
                print(f"Description: {description}")
                print(f"Image Link: {image_url}")

                create_image(title, image_url)

                keyboard = [[telegram.InlineKeyboardButton("JOIN US 🔥", url=JOIN_URL)]]
                reply_markup = telegram.InlineKeyboardMarkup(keyboard)
                message = f"<b>{title}</b>\n\n{description}"

                context.bot.send_photo(chat_id=CHAT_ID, photo=open(POST_IMAGE_PATH, 'rb'),
                                       caption=message[:1000], parse_mode='html', reply_markup=reply_markup)
            except Exception as e:
                print(f"Error: {e}")


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    send_post(context=updater)


if __name__ == "__main__":
    main()

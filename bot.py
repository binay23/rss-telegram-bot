import feedparser
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

feed = feedparser.parse("https://www.firstpost.com/commonfeeds/v1/mfp/rss/home.xml")

entry = feed.entries[0]

title = entry.title
summary = entry.summary[:200]

# Try to get image
image_url = None
if "media_content" in entry:
    image_url = entry.media_content[0]['url']

if not image_url:
    image_url = "https://via.placeholder.com/800x400.png?text=News"

# Download image
response = requests.get(image_url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# Add watermark
draw = ImageDraw.Draw(img)
text = "SSB JUNCTION"
width, height = img.size

draw.text((width-250, height-40), text, fill=(255,255,255))

# Save image
img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

caption = f"📰 {title}\n\n🧾 {summary}"

with open("news.jpg", "rb") as photo:
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "caption": caption
    }, files={"photo": photo})

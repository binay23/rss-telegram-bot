import feedparser
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import os
import re

# Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Google News RSS (India defence + international)
RSS_URL = "https://news.google.com/rss/search?q=india+defence+OR+india+military+OR+india+international+relations&hl=en-IN&gl=IN&ceid=IN:en"

feed = feedparser.parse(RSS_URL)

if not feed.entries:
    print("No news found")
    exit()

entry = feed.entries[0]

# Title
title = entry.title

# Clean summary
summary_raw = entry.summary if "summary" in entry else ""
summary = re.sub('<.*?>', '', summary_raw)
summary = summary[:200]

# Image handling
image_url = None
if "media_content" in entry:
    try:
        image_url = entry.media_content[0]['url']
    except:
        image_url = None

# Fallback image
if not image_url:
    image_url = "https://via.placeholder.com/800x400.png?text=SSB+Junction"

# Download image
response_img = requests.get(image_url)
img = Image.open(BytesIO(response_img.content)).convert("RGB")

# Add watermark
draw = ImageDraw.Draw(img)
width, height = img.size
draw.text((width - 220, height - 40), "SSB JUNCTION", fill=(255, 255, 255))

# Save image
img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

caption = f"🪖 {title}\n\n🌍 {summary}"

with open("news.jpg", "rb") as photo:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={
            "photo": photo
        }
    )

# Final log
print("Telegram response:", response.text)
response = requests.get(image_url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# Watermark
draw = ImageDraw.Draw(img)
width, height = img.size
draw.text((width-220, height-40), "SSB JUNCTION", fill=(255,255,255))

img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
caption = f"🪖 {title}\n\n🌍 {summary}"

with open("news.jpg", "rb") as photo:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={"photo": photo}
    )

print("Telegram response:", response.text)        pass

if not image_url:
    image_url = "https://via.placeholder.com/800x400.png?text=SSB+Junction"

# Download image
response = requests.get(image_url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# Watermark
draw = ImageDraw.Draw(img)
width, height = img.size
draw.text((width-220, height-40), "SSB JUNCTION", fill=(255,255,255))

# Save image
img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

caption = f"🪖 {title}\n\n🌍 {summary}"

with open("news.jpg", "rb") as photo:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={"photo": photo}
    )

print("Telegram response:", response.text)

with open("news.jpg", "rb") as photo:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption
        },
        files={"photo": photo}
    )

print("Telegram response:", response.text)    requests.post(url, data={
        "chat_id": CHAT_ID,
        "caption": caption
    }, files={"photo": photo})

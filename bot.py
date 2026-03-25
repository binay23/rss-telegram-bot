import feedparser
import requests
from PIL import Image, ImageDraw
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
title = entry.title[:80]

# Clean summary
summary_raw = entry.summary if "summary" in entry else ""
summary = re.sub('<.*?>', '', summary_raw)
summary = summary[:150]

# Create image (NO INTERNET NEEDED)
img = Image.new('RGB', (800, 400), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Add text
draw.text((20, 40), "🪖 NEWS", fill=(255, 255, 255))
draw.text((20, 100), title, fill=(255, 255, 255))
draw.text((20, 200), summary, fill=(200, 200, 200))

# Watermark
draw.text((550, 350), "SSB JUNCTION", fill=(255, 255, 255))

# Save image
img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

with open("news.jpg", "rb") as photo:
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": "🪖 Defence & International Update"
        },
        files={"photo": photo}
    )

print("Telegram response:", response.text)
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

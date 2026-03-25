import feedparser
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

feed = feedparser.parse("https://www.firstpost.com/commonfeeds/v1/mfp/rss/home.xml")

if not feed.entries:
    print("No entries found")
    exit()

entry = feed.entries[0]

title = entry.title
summary = entry.summary[:200] if "summary" in entry else "No summary available"

# Safe image extraction
image_url = None

if "media_content" in entry:
    try:
        image_url = entry.media_content[0]['url']
    except:
        pass

if not image_url:
    image_url = "https://via.placeholder.com/800x400.png?text=SSB+Junction"

# Download image
response = requests.get(image_url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# Add watermark
draw = ImageDraw.Draw(img)
width, height = img.size

draw.text((width-200, height-30), "SSB JUNCTION", fill=(255,255,255))

# Save image
img.save("news.jpg")

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

caption = f"📰 {title}\n\n🧾 {summary}"

with open("news.jpg", "rb") as photo:
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "caption": caption
    }, files={"photo": photo})

img.save("news.jpg")
print(r.text)

# Send to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

caption = f"📰 {title}\n\n🧾 {summary}"

with open("news.jpg", "rb") as photo:
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "caption": caption
    }, files={"photo": photo})

import feedparser
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_URL = "https://news.google.com/rss/search?q=india+defence+OR+india+military+OR+india+international+relations&hl=en-IN&gl=IN&ceid=IN:en"

feed = feedparser.parse(RSS_URL)

if not feed.entries:
    print("No news found")
    exit()

entry = feed.entries[0]

title = entry.title

summary_raw = entry.summary if "summary" in entry else ""
summary = re.sub('<.*?>', '', summary_raw)
summary = summary[:200]

image_url = "https://via.placeholder.com/800x400.png?text=SSB+Junction"

response_img = requests.get(image_url)
img = Image.open(BytesIO(response_img.content)).convert("RGB")

draw = ImageDraw.Draw(img)
width, height = img.size
draw.text((width - 220, height - 40), "SSB JUNCTION", fill=(255, 255, 255))

img.save("news.jpg")

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

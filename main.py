import requests
from bs4 import BeautifulSoup
import os
import json
from googletrans import Translator
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

BASE_URL = "https://www.encar.com"
MEDIA_URL = "https://www.encar.com/mg/index.do"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

translator = Translator()

def get_articles():
    r = requests.get(MEDIA_URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    items = soup.select(".list_area li")[:6]

    for item in items:
        title_kr = item.select_one(".tit").get_text(strip=True)
        link = BASE_URL + item.select_one("a")["href"]
        articles.append((title_kr, link))

    return articles

def load_posted():
    if os.path.exists("posted.json"):
        with open("posted.json", "r") as f:
            return json.load(f)
    return []

def save_posted(data):
    with open("posted.json", "w") as f:
        json.dump(data, f)

def translate(text):
    return translator.translate(text, src="ko", dest="ru").text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

def main():
    send_to_telegram("✅ Тестовое сообщение. Бот работает.")


if __name__ == "__main__":
    main()

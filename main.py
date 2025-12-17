import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

BASE_URL = "https://www.encar.com"
MEDIA_URL = "https://m.encar.com/mg/index.do"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
}

translator = Translator()

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
    r = requests.get(MEDIA_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = soup.select("a[href*='/mg/']")[:5]

    if not articles:
        send_to_telegram("❌ Encar: новости не найдены")
        return

    date = datetime.now().strftime("%d.%m.%Y")
    message = f"🚗 <b>Автоновости Encar — {date}</b>\n\n"

    for i, a in enumerate(articles, 1):
        title_kr = a.get_text(strip=True)
        link = BASE_URL + a["href"]

        if len(title_kr) < 8:
            continue

        title_ru = translator.translate(title_kr, src="ko", dest="ru").text
        message += f"{i}️⃣ <b>{title_ru}</b>\n{link}\n\n"

    send_to_telegram(message)

if __name__ == "__main__":
    main()

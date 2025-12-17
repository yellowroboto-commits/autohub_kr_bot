import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

URL = "https://m.encar.com/mg/index.do"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": False
    })

def main():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.select("a[href*='/mg/']")[:5]

    if not links:
        send("⚠️ Encar: новости не найдены")
        return

    date = datetime.now().strftime("%d.%m.%Y")
    msg = f"🚗 Encar — авто новости ({date})\n\n"

    used = set()

    for i, a in enumerate(links, 1):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or href in used:
            continue

        used.add(href)
        msg += f"{i}. {title}\nhttps://www.encar.com{href}\n\n"

    send(msg)

if __name__ == "__main__":
    main()

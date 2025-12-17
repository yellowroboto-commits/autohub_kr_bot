import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": text
    })

def main():
    send("🟡 Шаг 1: код запустился")

    try:
        r = requests.get(
            "https://m.encar.com/mg/index.do",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        send("🟢 Шаг 2: сайт открыт, код " + str(r.status_code))
        send("📄 Длина HTML: " + str(len(r.text)))
    except Exception as e:
        send("🔴 Ошибка запроса: " + str(e))
        return

    send("✅ Шаг 3: выполнение завершено")

if __name__ == "__main__":
    main()

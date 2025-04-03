
import openai
import requests
from flask import Flask, request
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" not in data:
        return {"ok": True}
    
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "")

    if not user_text:
        send_telegram(chat_id, "Пока я понимаю только текстовые сообщения 😊")
        return {"ok": True}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "Произошла ошибка при обращении к GPT 😓"

    send_telegram(chat_id, reply)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

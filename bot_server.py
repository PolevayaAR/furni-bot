
from flask import Flask, request
import openai
import os
import requests

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ASSISTANT_ID = "asst_t9WvDzn8o9Tnlr56RZHHhoqN"

thread_store = {}  # можно заменить на базу или Redis

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    if not chat_id or not text:
        return "ok"

    # Создаём или используем thread для этого чата
    if chat_id not in thread_store:
        thread = client.beta.threads.create()
        thread_store[chat_id] = thread.id
    thread_id = thread_store[chat_id]

    # Отправляем сообщение в thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text
    )

    # Запускаем ассистента
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Ждём завершения
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            send_telegram(chat_id, "Ошибка: ассистент не смог ответить 😢")
            return "ok"

    # Получаем ответ
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "🤖 Нет ответа")

    send_telegram(chat_id, reply)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Furni Buddy Assistant is live!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

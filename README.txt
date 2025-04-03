
🚀 FURNI BOT — Telegram ↔ GPT

1. Зайди на Railway → "New Project" → "Deploy template" → "Blank project"
2. Загрузите все файлы из этого архива
3. Перейди во вкладку "Variables" и добавь:

TELEGRAM_TOKEN=твой_токен
OPENAI_API_KEY=твой_ключ

4. Перейди в "Deployments → Settings" и убедись, что стартовая команда:
web: python bot_server.py

5. После запуска возьми URL проекта, например:
https://furni-bot-production.up.railway.app

6. Привяжи Telegram бот:
curl -F "url=https://.../webhook" https://api.telegram.org/bot<токен>/setWebhook

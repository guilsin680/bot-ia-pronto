import os
import requests

def enviar_telegram(mensagem):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": mensagem}
        requests.post(url, data=payload)
    else:
        print("❌ Variáveis de ambiente do Telegram não configuradas.")
import os
import requests
import pandas as pd

API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def buscar_jogos_hoje():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {
        "date": pd.Timestamp.today().strftime('%Y-%m-%d'),
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    jogos = []
    for item in data.get("response", []):
        jogos.append({
            "league": item["league"]["name"],
            "home_team": item["teams"]["home"]["name"],
            "away_team": item["teams"]["away"]["name"],
            "home_goals": 1,  # valor fictício, substitua se tiver dados reais
            "away_goals": 2,
            "date": item["fixture"]["date"][:10],
            "time": item["fixture"]["date"][11:16],
        })

    return jogos

def enviar_mensagem(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

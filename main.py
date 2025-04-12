import os
import requests
from flask import Flask
from predictor import prever_resultado
from telegram_alert import enviar_telegram

app = Flask(__name__)

# Função para pegar jogos de hoje usando a API-Football
def obter_jogos_hoje():
    api_key = os.getenv("API_FOOTBALL_KEY")
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }
    params = {"date": "2025-04-11"}  # Data fixa para o dia de hoje, você pode ajustar conforme necessário
    response = requests.get(url, headers=headers, params=params)
    jogos = response.json().get('response', [])
    return jogos

@app.route('/')
def home():
    jogos_hoje = obter_jogos_hoje()
    for jogo in jogos_hoje:
        home_team = jogo['teams']['home']['name']
        away_team = jogo['teams']['away']['name']
        home_goals = jogo['goals']['home']
        away_goals = jogo['goals']['away']

        # Gerar previsão para cada jogo
        resultado = prever_resultado(home_goals, away_goals)

        # Enviar previsão para o Telegram
        mensagem = f"⚽ {home_team} vs {away_team} → {resultado}"
        enviar_telegram(mensagem)
    
    return '✅ Previsões enviadas para o Telegram com sucesso!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

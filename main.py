import os
import requests
import pickle
from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)

# Configurações
API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Função para buscar jogos de hoje na API-Football
def buscar_jogos_hoje():
    hoje = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&status=NS"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("response", [])

# Função para enviar mensagem ao Telegram
def enviar_mensagem_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}
    requests.post(url, data=payload)

# Função para simular previsão com IA
def prever_resultado(jogo):
    # Simulação de IA (pode usar seu modelo real aqui)
    return {
        "previsao": "Casa vence",
        "confianca": "Alta"
    }

# Rota principal
@app.route("/")
def bot():
    jogos = buscar_jogos_hoje()
    if not jogos:
        enviar_mensagem_telegram("Nenhum jogo encontrado para hoje.")
        return "Sem jogos"

    for jogo in jogos[:5]:  # Limita para evitar spam
        home = jogo["teams"]["home"]["name"]
        away = jogo["teams"]["away"]["name"]
        liga = jogo["league"]["name"]
        data_hora_utc = jogo["fixture"]["date"]
        data_hora_br = datetime.fromisoformat(data_hora_utc[:-1]).astimezone(pytz.timezone("America/Sao_Paulo"))
        horario = data_hora_br.strftime("%d/%m/%Y às %H:%M")

        previsao = prever_resultado(jogo)
        texto = (
            f"<b>⚽ Previsão de Jogo</b>\n"
            f"<b>Partida:</b> {home} x {away}\n"
            f"<b>Liga:</b> {liga}\n"
            f"<b>Data/Horário:</b> {horario}\n"
            f"<b>Previsão IA:</b> {previsao['previsao']}\n"
            f"<b>Confiança:</b> {previsao['confianca']}"
        )
        enviar_mensagem_telegram(texto)

    return "Mensagens enviadas"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

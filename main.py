import requests
import pickle
from flask import Flask
from datetime import datetime
import pytz
from dateutil import parser
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

# Função para enviar mensagens para o Telegram
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# Função para buscar os jogos de hoje
def buscar_jogos_hoje():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_FOOTBALL_KEY
    }

    hoje = datetime.utcnow().strftime("%Y-%m-%d")
    params = {
        "date": hoje,
        "timezone": "UTC"
    }

    resposta = requests.get(url, headers=headers, params=params)
    dados = resposta.json()
    return dados.get("response", [])

# Função para prever resultado de uma partida
def prever_partida(jogo, modelo):
    home_goals = jogo["goals"]["home"]
    away_goals = jogo["goals"]["away"]

    # Simulação de entrada (usar IA real depois)
    entrada = [[home_goals or 0, away_goals or 0]]
    resultado = modelo.predict(entrada)[0]
    prob = modelo.predict_proba(entrada).max()

    return resultado, prob

# Rota principal
@app.route("/")
def bot():
    try:
        with open("modelo.pkl", "rb") as f:
            modelo = pickle.load(f)

        jogos = buscar_jogos_hoje()

        if not jogos:
            enviar_telegram("Nenhum jogo encontrado para hoje.")
            return "Sem jogos hoje."

        for jogo in jogos:
            resultado, confianca = prever_partida(jogo, modelo)

            # Infos detalhadas do jogo
            data_hora_utc = jogo["fixture"]["date"]
            data_hora_br = parser.isoparse(data_hora_utc).astimezone(pytz.timezone("America/Sao_Paulo"))
            data_formatada = data_hora_br.strftime("%d/%m/%Y %H:%M")

            casa = jogo["teams"]["home"]["name"]
            visitante = jogo["teams"]["away"]["name"]
            liga = jogo["league"]["name"]

            msg = (
                f"<b>Jogo:</b> {casa} vs {visitante}\n"
                f"<b>Data/Hora:</b> {data_formatada}\n"
                f"<b>Liga:</b> {liga}\n"
                f"<b>Previsão:</b> {resultado}\n"
                f"<b>Confiança:</b> {confianca:.2%}"
            )

            enviar_telegram(msg)

        return "Previsões enviadas com sucesso."

    except Exception as e:
        enviar_telegram(f"Erro no bot: {e}")
        return f"Erro: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

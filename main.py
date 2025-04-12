import requests
import pickle
from datetime import datetime
import pytz
from flask import Flask
import os

app = Flask(__name__)

# Carrega modelo e encoders
with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)
with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Variáveis de ambiente
API_KEY = os.getenv("API_FOOTBALL_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def buscar_jogos_hoje():
    url = "https://v3.football.api-sports.io/fixtures?date={}".format(datetime.today().strftime('%Y-%m-%d'))
    headers = {"x-apisports-key": API_KEY}
    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    return dados["response"]

def prever_jogos(jogos):
    mensagens = []

    for jogo in jogos:
        home = jogo['teams']['home']['name']
        away = jogo['teams']['away']['name']
        liga = jogo['league']['name']
        data_hora_utc = jogo['fixture']['date']

        try:
            data_hora = datetime.fromisoformat(data_hora_utc.replace('Z', '+00:00')).astimezone(pytz.timezone("America/Sao_Paulo"))
        except Exception:
            data_hora = data_hora_utc

        if home in encoders['home'].classes_ and away in encoders['away'].classes_:
            home_encoded = encoders['home'].transform([home])[0]
            away_encoded = encoders['away'].transform([away])[0]

            entrada = [[home_encoded, away_encoded, 0, 0]]
            pred = model.predict(entrada)[0]
            probs = model.predict_proba(entrada)[0]
            confianca = round(max(probs) * 100, 2)

            if pred == 0:
                resultado = f"{home} vence"
            elif pred == 1:
                resultado = "Empate"
            else:
                resultado = f"{away} vence"

            msg = (
                f"**Previsão de Jogo**\n"
                f"📅 {data_hora.strftime('%d/%m/%Y %H:%M')}\n"
                f"🏆 {liga}\n"
                f"⚽ {home} x {away}\n"
                f"🧠 Previsão: *{resultado}*\n"
                f"🔍 Confiança: {confianca}%"
            )
            mensagens.append(msg)
    return mensagens

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

@app.route('/')
def bot():
    try:
        jogos = buscar_jogos_hoje()
        mensagens = prever_jogos(jogos)
        if mensagens:
            for msg in mensagens:
                enviar_telegram(msg)
            return "Mensagens enviadas com sucesso!"
        else:
            enviar_telegram("Nenhum jogo disponível hoje para previsão.")
            return "Nenhum jogo disponível hoje."
    except Exception as e:
        enviar_telegram(f"Erro ao executar bot: {e}")
        return f"Erro interno: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

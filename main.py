import os
import requests
from flask import Flask
from datetime import datetime
from predictor import prever_resultado
from api_football import buscar_jogos

app = Flask(__name__)

@app.route('/')
def home():
    # Pega os jogos do dia atual usando a API-Football
    jogos = buscar_jogos()

    mensagens = []

    for jogo in jogos:
        # Faz a previsão com o modelo de IA
        resultado = prever_resultado(jogo)

        # Cria uma mensagem detalhada
        mensagem = f"""
        ⚽ **Previsão do jogo**
        🏟️ **{jogo['home_team']} x {jogo['away_team']}**
        🕑 **Data e Hora**: {jogo['date']} (Horário de Brasília)
        🏆 **Liga**: {jogo['league']}
        
        **Previsão**: {resultado['prediction']}
        **Confiança da previsão**: {resultado['confidence']}%

        🔗 **Link para o jogo**: [Veja mais detalhes](https://www.betfair.com)
        """
        mensagens.append(mensagem)

    # Envia as mensagens para o Telegram
    enviar_telegram("\n\n".join(mensagens))

    return '✅ Previsões enviadas para o Telegram com sucesso!'

def enviar_telegram(mensagem):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
    else:
        print("❌ Variáveis de ambiente do Telegram não configuradas.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

import os
import requests
import json
from datetime import datetime
from telegram import Bot

# Função para obter os jogos do dia
def obter_jogos():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "7d42d1204d937e99f1139bdd3c845c48"  
    params = {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "timezone": "America/Sao_Paulo"
    }
    response = requests.get(url, headers=headers, params=params)
    jogos = response.json()['response']
    return jogos

# Função para formatar a mensagem
def formatar_mensagem(jogo, resultado_previsto):
    time_casa = jogo['teams']['home']['name']
    time_fora = jogo['teams']['away']['name']
    data = jogo['fixture']['date']
    liga = jogo['league']['name']
    hora = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z").strftime('%H:%M:%S')
    
    # Mensagem formatada
    mensagem = (f"⚽ **Jogo:** {time_casa} x {time_fora}\n"
                f"📅 **Data:** {data[:10]} | ⏰ **Hora:** {hora}\n"
                f"🏆 **Liga:** {liga}\n"
                f"🔮 **Resultado Previsto:** {resultado_previsto}\n"
                f"Confiança: Alta\n")
    return mensagem

# Função para enviar mensagem no Telegram
def enviar_telegram(mensagem):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if bot_token and chat_id:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")
    else:
        print("❌ Variáveis de ambiente do Telegram não configuradas.")

# Função para prever o resultado com base em uma lógica simples (Exemplo simples)
def prever_resultado(jogo):
    # A previsão simples será sempre uma vitória do time da casa (alterar conforme necessário)
    return "Vitória do time da casa"

# Função para enviar as previsões de todos os jogos do dia
def enviar_previsao():
    jogos = obter_jogos()
    
    for jogo in jogos:
        resultado_previsto = prever_resultado(jogo)
        mensagem = formatar_mensagem(jogo, resultado_previsto)
        enviar_telegram(mensagem)

if __name__ == "__main__":
    enviar_previsao()


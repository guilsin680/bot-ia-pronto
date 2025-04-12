from flask import Flask
from predictor import buscar_jogos_hoje, prever_resultados
from telegram_alert import enviar_telegram

app = Flask(__name__)

@app.route('/')
def home():
    jogos_hoje = buscar_jogos_hoje()
    
    if jogos_hoje:
        previsao = prever_resultados(jogos_hoje)
        mensagem = "\n".join(previsao)
        enviar_telegram(f"⚽ Previsões dos jogos de hoje:\n\n{mensagem}")
        return '✅ Previsões enviadas para o Telegram com sucesso!'
    else:
        return '❌ Não foi possível obter os jogos de hoje.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

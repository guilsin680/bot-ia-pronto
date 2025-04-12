from flask import Flask
from predictor import prever_resultado
from telegram_alert import enviar_telegram

app = Flask(__name__)

@app.route('/')
def home():
    resultado = prever_resultado()
    enviar_telegram(f'⚽ Previsão do jogo: {resultado}')
    return '✅ Previsão enviada para o Telegram com sucesso!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
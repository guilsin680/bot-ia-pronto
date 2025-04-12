import requests
import os
from datetime import datetime

API_KEY = os.getenv("API_FOOTBALL_KEY")

def prever_resultado():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timezone": "America/Sao_Paulo",
        "status": "NS"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "response" not in data or not data["response"]:
        return "Nenhum jogo encontrado para hoje."

    mensagem_final = "📊 *Previsões para hoje:*\n\n"

    for jogo in data["response"][:5]:  # mostra no máximo 5 jogos por vez
        info = jogo["fixture"]
        league = jogo["league"]
        teams = jogo["teams"]

        data_jogo = datetime.strptime(info["date"], "%Y-%m-%dT%H:%M:%S%z")
        horario = data_jogo.strftime("%H:%M")
        data_formatada = data_jogo.strftime("%d/%m/%Y")

        casa = teams["home"]["name"]
        fora = teams["away"]["name"]

        # Simulação de previsão
        import random
        resultado_previsto = random.choice(["Vitória do mandante", "Empate", "Vitória do visitante"])
        confianca = round(random.uniform(60, 90), 2)

        mensagem_final += (
            f"🏟️ {casa} x {fora}\n"
            f"📅 {data_formatada} ⏰ {horario}\n"
            f"🏆 {league['name']} ({league['country']})\n"
            f"🔮 Previsão: *{resultado_previsto}*\n"
            f"✅ Confiança: *{confianca}%*\n"
            f"───────────────\n"
        )

    return mensagem_final

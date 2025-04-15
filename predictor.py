import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from api import buscar_jogos_hoje, enviar_mensagem

def treinar_modelo():
    df = pd.read_csv("historico.csv")

    df["vencedor"] = df.apply(lambda row: "casa" if row["home_goals"] > row["away_goals"]
                               else "fora" if row["away_goals"] > row["home_goals"] else "empate", axis=1)

    X = df[["home_goals", "away_goals"]]
    y = df["vencedor"]

    modelo = RandomForestClassifier()
    modelo.fit(X, y)

    with open("modelo.pkl", "wb") as f:
        pickle.dump(modelo, f)

def prever_partidas(modelo):
    jogos = buscar_jogos_hoje()

    mensagens = []

    for jogo in jogos:
        entrada = [[jogo["home_goals"], jogo["away_goals"]]]
        pred = modelo.predict(entrada)[0]
        prob = modelo.predict_proba(entrada).max()

        msg = (
            f"**{jogo['league']}**\n"
            f"{jogo['home_team']} x {jogo['away_team']}\n"
            f"Data: {jogo['date']} - {jogo['time']}\n"
            f"Previsão: {pred.upper()} (Confiança: {prob:.2%})"
        )
        mensagens.append(msg)

    for m in mensagens:
        enviar_mensagem(m)

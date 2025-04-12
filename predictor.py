import pickle
import numpy as np

# Carregar o modelo treinado
def carregar_modelo():
    with open('modelo_ia.pkl', 'rb') as f:
        modelo = pickle.load(f)
    return modelo

# Função para prever o resultado
def prever_resultado(jogo):
    modelo = carregar_modelo()

    # Extrair as variáveis para a previsão (ajuste conforme o modelo)
    features = np.array([jogo['home_goals'], jogo['away_goals'], jogo['home_team_rank'], jogo['away_team_rank']]).reshape(1, -1)

    resultado = modelo.predict(features)
    confianca = modelo.predict_proba(features).max() * 100

    return {'prediction': resultado[0], 'confidence': confianca}


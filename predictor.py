import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

# Carregar o arquivo CSV com dados de partidas (pode manter como exemplo para treino inicial)
def carregar_dados():
    df = pd.read_csv('data.csv')
    return df

# Treinamento e previsão com o modelo
def treinar_modelo():
    df = carregar_dados()
    X = df[['home_goals', 'away_goals']]  # Características de gols
    y = df['result']  # Resultado do jogo (exemplo: 1 = vitória do time da casa)

    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Normalização dos dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Treinar o modelo
    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    # Salvar o modelo treinado
    with open('modelo.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    return modelo

# Carregar o modelo treinado
def carregar_modelo():
    try:
        with open('modelo.pkl', 'rb') as f:
            modelo = pickle.load(f)
    except FileNotFoundError:
        modelo = treinar_modelo()  # Se o modelo não existir, treine um novo
    return modelo

# Fazer uma previsão
def prever_resultado(home_goals, away_goals):
    modelo = carregar_modelo()
    dados_novos = np.array([[home_goals, away_goals]])  # Gols de casa vs fora
    resultado = modelo.predict(dados_novos)
    return 'Vitória do time da casa' if resultado[0] == 1 else 'Vitória do time visitante'

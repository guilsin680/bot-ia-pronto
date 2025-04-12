import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

def carregar_dados():
    df = pd.read_csv('data.csv')
    df['result'] = df['result'].map({'Home': 1, 'Away': 0, 'Draw': 2})
    return df

def treinar_modelo():
    df = carregar_dados()
    X = df[['home_goals', 'away_goals']]
    y = df['result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    with open('modelo.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    return modelo

def carregar_modelo():
    try:
        with open('modelo.pkl', 'rb') as f:
            modelo = pickle.load(f)
    except FileNotFoundError:
        modelo = treinar_modelo()
    return modelo

def prever_resultado():
    modelo = carregar_modelo()
    dados_novos = np.array([[1, 2]])  # Exemplo de entrada
    resultado = modelo.predict(dados_novos)
    if resultado[0] == 1:
        return 'Vitória do time da casa'
    elif resultado[0] == 0:
        return 'Vitória do time visitante'
    else:
        return 'Empate'
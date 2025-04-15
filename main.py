import os
import pickle
from predictor import treinar_modelo, prever_partidas

# Verifica se o modelo já existe
if not os.path.exists("modelo.pkl"):
    print("Modelo não encontrado. Treinando novo modelo...")
    treinar_modelo()

# Carrega o modelo treinado
with open('modelo.pkl', 'rb') as f:
    modelo = pickle.load(f)

# Executa as previsões
prever_partidas(modelo)

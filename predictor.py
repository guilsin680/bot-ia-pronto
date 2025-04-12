import requests
from datetime import datetime

API_KEY = '7d42d1204d937e99f1139bdd3c845c48'  # Sua chave da API-Football
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'

def buscar_jogos_hoje():
    url = f'{BASE_URL}/fixtures'
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
    }
    params = {
        'date': datetime.today().strftime('%Y-%m-%d'),  # Data de hoje
        'timezone': 'America/Sao_Paulo'
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        jogos = response.json()['response']
        return jogos
    else:
        return []

def prever_resultados(jogos):
    # Aqui você pode colocar a lógica de IA para prever os resultados
    previsao = []
    for jogo in jogos:
        time_casa = jogo['teams']['home']['name']
        time_fora = jogo['teams']['away']['name']
        # Prevendo baseado apenas no nome dos times (ajuste a lógica conforme o seu modelo de IA)
        resultado = 'Casa'  # Supondo que você tenha um modelo que decida entre 'Casa', 'Fora', 'Empate'
        previsao.append(f"{time_casa} vs {time_fora} -> Vitória do {resultado}")
    return previsao


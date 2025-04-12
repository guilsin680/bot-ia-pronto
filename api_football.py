import os
import requests

def buscar_jogos():
    api_key = os.getenv('API_FOOTBALL_KEY')
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={datetime.now().strftime('%Y-%m-%d')}"
    
    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }

    response = requests.get(url, headers=headers)
    jogos = response.json()['response']

    jogos_filtrados = []
    for jogo in jogos:
        jogos_filtrados.append({
            'home_team': jogo['teams']['home']['name'],
            'away_team': jogo['teams']['away']['name'],
            'date': jogo['fixture']['date'],
            'league': jogo['league']['name']
        })

    return jogos_filtrados

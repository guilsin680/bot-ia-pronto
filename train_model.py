import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Carrega o CSV com dados reais
df = pd.read_csv('dados_partidas.csv')  # Precisa conter colunas: home_team, away_team, home_goals, away_goals, result

# Codifica os times
le_home = LabelEncoder()
le_away = LabelEncoder()
df['home_team'] = le_home.fit_transform(df['home_team'])
df['away_team'] = le_away.fit_transform(df['away_team'])

# Define variáveis
X = df[['home_team', 'away_team', 'home_goals', 'away_goals']]
y = df['result']  # 0 = casa vence, 1 = empate, 2 = fora vence

# Treina o modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salva o modelo
with open('modelo.pkl', 'wb') as f:
    pickle.dump(model, f)

# Salva os encoders
with open('encoders.pkl', 'wb') as f:
    pickle.dump({'home': le_home, 'away': le_away}, f)

print("Modelo e encoders salvos com sucesso.")

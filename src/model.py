import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load and prepare the model
def load_model():
    csv_path = resource_path('data/results.csv')
    df = pd.read_csv(csv_path)
    df = df[['home_team', 'away_team', 'home_score', 'away_score']]

    def get_results(row):
        if row['home_score'] > row['away_score']:
            return 'Win'
        elif row['home_score'] == row['away_score']:
            return 'Draw'
        else:
            return 'Loss'

    df['Result'] = df.apply(get_results, axis=1)

    home_teams = pd.get_dummies(df['home_team'], prefix='Home')
    away_teams = pd.get_dummies(df['away_team'], prefix='Away')
    x = pd.concat([home_teams, away_teams], axis=1)
    y = df['Result']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    return model, x

# Predict a match
def predict_match(model, x, home_team, away_team):
    new_match = pd.DataFrame(0, index=[0], columns=x.columns)

    if f'Home_{home_team}' not in new_match.columns or f'Away_{away_team}' not in new_match.columns:
        raise ValueError("Team not found in training data.")

    new_match[f'Home_{home_team}'] = 1
    new_match[f'Away_{away_team}'] = 1

    probabilities = model.predict_proba(new_match)[0]
    classes = model.classes_

    return dict(zip(classes, probabilities))

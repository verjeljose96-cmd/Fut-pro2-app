import requests
import pandas as pd
import os

API_KEY = "1ebf9cc134674f68bfc2c86bf9e8c8f7"

HEADERS = {
    "X-Auth-Token": API_KEY
}

LEAGUES = {
    "premier_league": "PL",
    "la_liga": "PD",
    "serie_a": "SA",
    "bundesliga": "BL1",
    "ligue_1": "FL1"
}

def update_league(league_name, league_code):

    url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error descargando {league_name}")
        return

    data = response.json()

    teams = {}

    for match in data["matches"][-100:]:

        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        home_goals = match["score"]["fullTime"]["home"]
        away_goals = match["score"]["fullTime"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if home not in teams:
            teams[home] = {"gf": [], "ga": []}

        if away not in teams:
            teams[away] = {"gf": [], "ga": []}

        teams[home]["gf"].append(home_goals)
        teams[home]["ga"].append(away_goals)

        teams[away]["gf"].append(away_goals)
        teams[away]["ga"].append(home_goals)

    rows = []

    for team, stats in teams.items():

        gf10 = sum(stats["gf"][-10:])
        ga10 = sum(stats["ga"][-10:])
        gf5 = sum(stats["gf"][-5:])
        ga5 = sum(stats["ga"][-5:])

        rows.append([team, gf10, ga10, gf5, ga5])

    df_final = pd.DataFrame(rows, columns=["Team", "GF10", "GA10", "GF5", "GA5"])

    os.makedirs("data", exist_ok=True)
    df_final.to_csv(f"data/{league_name}.csv", index=False)

    print(f"{league_name} actualizada correctamente.")


if __name__ == "__main__":

    for name, code in LEAGUES.items():
        update_league(name, code)

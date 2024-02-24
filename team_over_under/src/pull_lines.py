import requests
import json

API_KEY = "586d76a1d384f9bb19d1df537db8bec4"
URL = "https://api.the-odds-api.com/v4/sports"

with open('team_over_under/data/team_mappings.json') as f:
    team_mappings = json.load(f)

def pull_lines():
    response = requests.get(f"{URL}/basketball_nba/odds", params={"api_key": API_KEY, "regions": "us", "markets": "totals"})
    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

    with open('team_over_under/data/lines_raw.json') as f:
        data = json.load(f)

    lines = []
    for game in data:
        game_lines = []
        for book in game["bookmakers"]:
            game_lines.append(book["markets"][0]["outcomes"][0]["point"])
        consensus_line = max(set(game_lines), key=game_lines.count)
        lines.append({
            "home_team": team_mappings[game["home_team"]],
            "away_team": team_mappings[game["away_team"]],
            "line": consensus_line
        })

    with open('team_over_under/data/lines.json', 'w') as f:
        json.dump(lines, f)

if __name__ == "__main__":
    pull_lines()
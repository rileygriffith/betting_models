from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats

import json
import pandas as pd
import time
from datetime import date, timedelta
import requests

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

def pull_scoreboard():
    df = None
    days_delta = 0
    while days_delta < 60:
        days_delta += 1
        day = date.today() - timedelta(days=days_delta)
        print(f"scanning {day} for game data")
        result = json.loads(ScoreboardV2(game_date=day, day_offset=0, league_id="00").get_response())
        time.sleep(3) # Sleep to prevent rate limiting
        headers = pd.DataFrame(result["resultSets"][1]["headers"])
        boxscore_df = pd.DataFrame(result["resultSets"][1]["rowSet"], columns=headers[0])

        boxscore_df["GAME_DATE_EST"] = pd.to_datetime(boxscore_df["GAME_DATE_EST"])
        if len(boxscore_df):
            if df is None:
                df = boxscore_df
            else:
                print(f"game data found for {day}")
                df = pd.concat([df, boxscore_df], ignore_index=True)
        
    df.to_csv("team_over_under/data/scoreboard_last60_days.csv")

def pull_team_stats():
    for last_n_games in [20, 10, 5]:
        result = json.loads(LeagueDashTeamStats(last_n_games=last_n_games, per_mode_detailed="PerGame", measure_type_detailed_defense="Four Factors").get_response())
        time.sleep(3) # Sleep to prevent rate limiting
        headers = pd.DataFrame(result["resultSets"][0]["headers"])
        df = pd.DataFrame(result["resultSets"][0]["rowSet"], columns=headers[0])
        filename = f"last_{last_n_games}_team_stats_raw.csv"
        df.to_csv(f"team_over_under/data/{filename}")
    print(df)

if __name__ == "__main__":
    pull_scoreboard()
    pull_team_stats()
    pull_lines()
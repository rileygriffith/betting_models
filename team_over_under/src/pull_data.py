from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats

import json
import pandas as pd
import time
from datetime import date, timedelta

def pull_scoreboard():
    print("Pulling scoreboard info...")
    df = None
    days_delta = 0
    while days_delta < 100:
        days_delta += 1
        day = date.today() - timedelta(days=days_delta)
        print(f"scanning {day} for game data")
        result = json.loads(ScoreboardV2(game_date=day, day_offset=0, league_id="00").get_response())
        time.sleep(2) # Sleep to prevent rate limiting
        headers = pd.DataFrame(result["resultSets"][1]["headers"])
        boxscore_df = pd.DataFrame(result["resultSets"][1]["rowSet"], columns=headers[0])

        boxscore_df["GAME_DATE_EST"] = pd.to_datetime(boxscore_df["GAME_DATE_EST"])
        if len(boxscore_df):
            if df is None:
                df = boxscore_df
            else:
                df = pd.concat([df, boxscore_df], ignore_index=True)
        
    df.to_csv("team_over_under/data/scoreboard_historical.csv")

def pull_four_factors():
    print("Pulling team stats...")
    for last_n_games in [50, 20, 10, 5]:
        result = json.loads(LeagueDashTeamStats(last_n_games=last_n_games, per_mode_detailed="PerGame", measure_type_detailed_defense="Four Factors").get_response())
        time.sleep(2) # Sleep to prevent rate limiting
        headers = pd.DataFrame(result["resultSets"][0]["headers"])
        df = pd.DataFrame(result["resultSets"][0]["rowSet"], columns=headers[0])
        filename = f"last_{last_n_games}_four_factors.csv"
        df.to_csv(f"team_over_under/data/{filename}")

def pull_advanced():
    print("Pulling team stats...")
    for last_n_games in [50, 20, 10, 5]:
        result = json.loads(LeagueDashTeamStats(last_n_games=last_n_games, per_mode_detailed="PerGame", measure_type_detailed_defense="Advanced").get_response())
        time.sleep(2) # Sleep to prevent rate limiting
        headers = pd.DataFrame(result["resultSets"][0]["headers"])
        df = pd.DataFrame(result["resultSets"][0]["rowSet"], columns=headers[0])
        filename = f"last_{last_n_games}_advanced.csv"
        df.to_csv(f"team_over_under/data/{filename}")

if __name__ == "__main__":
    pull_scoreboard()
    pull_four_factors()
    pull_advanced()
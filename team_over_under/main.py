import pandas as pd
import json

df = pd.read_csv("team_over_under/data/1st_half_team_total.csv", index_col=0)
with open("team_over_under/data/lines.json") as f:
    lines = json.load(f)

output_df = pd.DataFrame(columns = ["TEAM", "1HL5", "1HL10", "1HL20"])


for game in lines:
    home_team = game["home_team"]
    away_team = game["away_team"]
    team_df = df

    team_df = team_df.loc[df["TEAM"] == home_team].head(20)
    print(f"Home Team: {home_team}")
    print(f"Average First Half Points: {team_df['PTS_1H'].mean()}")
    break
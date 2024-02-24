import pandas as pd
import json
import time
from datetime import date
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from team_over_under.src.process_data import process_scoreboard

def predict():
    result = json.loads(ScoreboardV2(game_date=date.today(), day_offset=0, league_id="00").get_response())
    time.sleep(1) # Sleep to prevent rate limiting
    headers = pd.DataFrame(result["resultSets"][1]["headers"])
    scoreboard_raw_df = pd.DataFrame(result["resultSets"][1]["rowSet"], columns=headers[0])

    scoreboard_raw_df = process_scoreboard(scoreboard_raw_df)
    scoreboard_raw_df["OPP_TEAM_ID"] = scoreboard_raw_df["OPP_TEAM_ID"].astype("str")

    output = {}
    for scope in [50, 20, 10, 5]:
        # Train model on last n
        df = pd.read_csv(f"team_over_under/data/last_{scope}_team_stats.csv", index_col=0)
        df = df.dropna()

        df_1h = df["PTS_1H"]
        df_total = df["PTS"]
        pts_averages_df = df.groupby("TEAM").mean()[["PTS_1H", "PTS"]]
        df.drop(["PTS_1H", "PTS", "TEAM"], axis=1, inplace=True)

        model_1h = LinearRegression()
        model_1h.fit(df, df_1h)
        model_total = LinearRegression()
        model_total.fit(df, df_total)

        rankings_df = pd.read_csv(f"team_over_under/data/last_{scope}_team_stats_raw.csv", index_col=0)
        scoreboard_df = scoreboard_raw_df
        # Join defensive stats to main df
        def_df = rankings_df[[
            "TEAM_ID",
            "OPP_EFG_PCT_RANK", "OPP_FTA_RATE_RANK",
            "OPP_TOV_PCT_RANK", "OPP_OREB_PCT_RANK",
        ]]
        def_df = def_df.rename({
            "OPP_EFG_PCT_RANK": f"OPP_EFG_PCT_RANK_LAST{scope}",
            "OPP_FTA_RATE_RANK": f"OPP_FTA_RATE_RANK_LAST{scope}",
            "OPP_TOV_PCT_RANK": f"OPP_TOV_PCT_RANK_LAST{scope}",
            "OPP_OREB_PCT_RANK": f"OPP_OREB_PCT_RANK_LAST{scope}",
        }, axis=1)
        scoreboard_df["OPP_TEAM_ID"] = scoreboard_df["TEAM_ID"].astype("str")
        def_df["TEAM_ID"] = def_df["TEAM_ID"].astype("str")
        scoreboard_df = scoreboard_df.join(def_df.set_index("TEAM_ID"), on="OPP_TEAM_ID")

        # Join offensive stats to main df
        off_df = rankings_df[[
            "TEAM_ID",
            "EFG_PCT_RANK", "FTA_RATE_RANK",
            "TM_TOV_PCT_RANK", "OREB_PCT_RANK",
        ]]
        off_df = off_df.rename({
            "EFG_PCT_RANK": f"EFG_PCT_RANK_LAST{scope}",
            "FTA_RATE_RANK": f"FTA_RATE_RANK_LAST{scope}",
            "TM_TOV_PCT_RANK": f"TOV_PCT_RANK_LAST{scope}",
            "OREB_PCT_RANK": f"OREB_PCT_RANK_LAST{scope}",
        }, axis=1)
        scoreboard_df = scoreboard_df.join(off_df.set_index("TEAM_ID"), on="TEAM_ID")

        scoreboard_df = scoreboard_df[[
            "TEAM", "HOME",
            f"EFG_PCT_RANK_LAST{scope}", f"FTA_RATE_RANK_LAST{scope}",
            f"TOV_PCT_RANK_LAST{scope}", f"OREB_PCT_RANK_LAST{scope}",
            f"OPP_EFG_PCT_RANK_LAST{scope}", f"OPP_FTA_RATE_RANK_LAST{scope}",
            f"OPP_TOV_PCT_RANK_LAST{scope}", f"OPP_OREB_PCT_RANK_LAST{scope}",
        ]]

        # Join 1h and total pts averages
        scoreboard_df = scoreboard_df.join(pts_averages_df, on="TEAM")
        scoreboard_df = scoreboard_df.rename({
            "PTS": "PTS_AVG",
            "PTS_1H": "PTS_1H_AVG",
        }, axis=1)

        for row in scoreboard_df.iterrows():
            index, data = row
            team = data['TEAM']
            output[team] = output.get(team, {})

            data = data.drop("TEAM").to_frame().T
            pred = model_1h.predict(data)[0]
            output[team][f"1H_{scope}"] = pred

            pred = model_total.predict(data)[0]
            output[team][f"T_{scope}"] = pred

    return output
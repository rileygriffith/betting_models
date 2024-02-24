import pandas as pd

from pull_data import pull_scoreboard, pull_team_stats, pull_lines

def process_data():
    print("Pulling scoreboard info, team stats, and lines...")
    # pull_scoreboard()
    # pull_team_stats()
    # pull_lines()
    print("Cleaning Data...")
    df = pd.read_csv("team_over_under/data/scoreboard_last60_days.csv", index_col=0, converters={"TEAM_ID": str})

    df = df.drop([
        "GAME_ID",
        "PTS_OT1",
        "PTS_OT2",
        "PTS_OT3",
        "PTS_OT4",
        "PTS_OT5",
        "PTS_OT6",
        "PTS_OT7",
        "PTS_OT8",
        "PTS_OT9",
        "PTS_OT10",
        "FG_PCT",
        "FT_PCT",
        "FG3_PCT",
        "AST",
        "REB",
        "TOV",
        "TEAM_CITY_NAME",
        "TEAM_NAME",
    ], axis=1)

    df["PTS_1H"] = df["PTS_QTR1"] + df["PTS_QTR2"]
    df = df.rename({"TEAM_ABBREVIATION": "TEAM"}, axis=1)

    for i, game in df.groupby(df.index // 2):
        index = i*2
        df.at[index, "HOME"] = False
        df.at[index+1, "HOME"] = True
        df.at[index, "OPP"] = df.at[index+1, "TEAM"]
        df.at[index, "OPP_TEAM_ID"] = df.at[index+1, "TEAM_ID"]
        df.at[index+1, "OPP"] = df.at[index, "TEAM"]
        df.at[index+1, "OPP_TEAM_ID"] = df.at[index, "TEAM_ID"]

    for scope in [20, 10, 5]:
        trend_df = pd.read_csv(f"team_over_under/data/last_{scope}_team_stats_raw.csv", index_col=0, converters={"TEAM_ID": str})

        # Join defensive stats to main df
        def_df = trend_df[[
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
        df = df.join(def_df.set_index("TEAM_ID"), on="OPP_TEAM_ID")

        # Join offensive stats to main df
        off_df = trend_df[[
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
        df = df.join(off_df.set_index("TEAM_ID"), on="TEAM_ID")

        dfx=df.groupby('TEAM').head(scope)
        dfx = dfx[[
            "TEAM", "PTS_1H", "PTS", "HOME",
            f"EFG_PCT_RANK_LAST{scope}", f"FTA_RATE_RANK_LAST{scope}",
            f"TOV_PCT_RANK_LAST{scope}", f"OREB_PCT_RANK_LAST{scope}",
            f"OPP_EFG_PCT_RANK_LAST{scope}", f"OPP_FTA_RATE_RANK_LAST{scope}",
            f"OPP_TOV_PCT_RANK_LAST{scope}", f"OPP_OREB_PCT_RANK_LAST{scope}",
        ]]
        print(dfx)
        dfx.to_csv(f"team_over_under/data/last_{scope}_team_stats.csv")

if __name__ == "__main__":
    process_data()
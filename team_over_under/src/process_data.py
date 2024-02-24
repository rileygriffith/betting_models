import pandas as pd

from pull_data import pull_scoreboard, pull_team_stats, pull_lines

def process_data():
    # pull_scoreboard()
    # pull_team_stats()
    # pull_lines()
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

    trend_df = pd.read_csv("team_over_under/data/last_5_team_stats.csv", index_col=0, converters={"TEAM_ID": str})
    trend_df = trend_df[[
        "TEAM_ID", "TEAM_NAME",
        "OPP_EFG_PCT_RANK", "OPP_FTA_RATE_RANK",
        "OPP_TOV_PCT_RANK", "OPP_OREB_PCT_RANK",
    ]]
    trend_df = trend_df.rename({
        "OPP_EFG_PCT_RANK": "OPP_EFG_PCT_RANK_LAST5",
        "OPP_FTA_RATE_RANK": "OPP_FTA_RATE_RANK_LAST5",
        "OPP_TOV_PCT_RANK": "OPP_TOV_PCT_RANK_LAST5",
        "OPP_OREB_PCT_RANK": "OPP_OREB_PCT_RANK_LAST5",
    }, axis=1)

    df = df.join(trend_df.set_index("TEAM_ID"), on="OPP_TEAM_ID")

    trend_df = pd.read_csv("team_over_under/data/last_10_team_stats.csv", index_col=0, converters={"TEAM_ID": str})
    trend_df = trend_df[[
        "TEAM_ID",
        "OPP_EFG_PCT_RANK", "OPP_FTA_RATE_RANK",
        "OPP_TOV_PCT_RANK", "OPP_OREB_PCT_RANK",
    ]]
    trend_df = trend_df.rename({
        "OPP_EFG_PCT_RANK": "OPP_EFG_PCT_RANK_LAST10",
        "OPP_FTA_RATE_RANK": "OPP_FTA_RATE_RANK_LAST10",
        "OPP_TOV_PCT_RANK": "OPP_TOV_PCT_RANK_LAST10",
        "OPP_OREB_PCT_RANK": "OPP_OREB_PCT_RANK_LAST10",
    }, axis=1)

    df = df.join(trend_df.set_index("TEAM_ID"), on="OPP_TEAM_ID")

    trend_df = pd.read_csv("team_over_under/data/last_20_team_stats.csv", index_col=0, converters={"TEAM_ID": str})
    trend_df = trend_df[[
        "TEAM_ID",
        "OPP_EFG_PCT_RANK", "OPP_FTA_RATE_RANK",
        "OPP_TOV_PCT_RANK", "OPP_OREB_PCT_RANK",
    ]]
    trend_df = trend_df.rename({
        "OPP_EFG_PCT_RANK": "OPP_EFG_PCT_RANK_LAST20",
        "OPP_FTA_RATE_RANK": "OPP_FTA_RATE_RANK_LAST20",
        "OPP_TOV_PCT_RANK": "OPP_TOV_PCT_RANK_LAST20",
        "OPP_OREB_PCT_RANK": "OPP_OREB_PCT_RANK_LAST20",
    }, axis=1)

    df = df.join(trend_df.set_index("TEAM_ID"), on="OPP_TEAM_ID")

    df = df[[
        "TEAM", "PTS_1H", "PTS", "HOME",
        "OPP_EFG_PCT_RANK_LAST5", "OPP_FTA_RATE_RANK_LAST5", "OPP_TOV_PCT_RANK_LAST5", "OPP_OREB_PCT_RANK_LAST5",
        "OPP_EFG_PCT_RANK_LAST10", "OPP_FTA_RATE_RANK_LAST10", "OPP_TOV_PCT_RANK_LAST10", "OPP_OREB_PCT_RANK_LAST10",
        "OPP_EFG_PCT_RANK_LAST20", "OPP_FTA_RATE_RANK_LAST20", "OPP_TOV_PCT_RANK_LAST20", "OPP_OREB_PCT_RANK_LAST20",
    ]]

    dfx=df.groupby('TEAM').head(20)
    import json
    with open("team_over_under/data/team_mappings.json") as f:
        teams = json.load(f)
    for key, value in teams.items():
        print(len(dfx.loc[dfx["TEAM"] == value]))

    # df.to_csv("team_over_under/data/1st_half_team_total.csv")

if __name__ == "__main__":
    process_data()
import pandas as pd
import json
import time
from datetime import date
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from src.process_data import clean_raw_data, join_team_stats


# df = pd.read_csv("team_over_under/data/last_20_team_stats.csv", index_col=0)
# df = df.dropna()

# df_1h = df["PTS_1H"]
# df_total = df["PTS"]
# df.drop(["PTS_1H", "PTS"], axis=1, inplace=True)
# print(df.columns)

# X_train, X_test, y_train, y_test = train_test_split(df, df_total, test_size=0.2, random_state=1)
# model = LinearRegression()
# print("Training Model")
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))

result = json.loads(ScoreboardV2(game_date=date.today(), day_offset=0, league_id="00").get_response())
time.sleep(2) # Sleep to prevent rate limiting
headers = pd.DataFrame(result["resultSets"][1]["headers"])
scoreboard_df = pd.DataFrame(result["resultSets"][1]["rowSet"], columns=headers[0])
scoreboard_df = clean_raw_data(scoreboard_df)
print(scoreboard_df)
scoreboard_df = join_team_stats(scoreboard_df, 20)

print(scoreboard_df)
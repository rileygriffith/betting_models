from team_over_under.predict import predict
from team_over_under.src.pull_data import pull_scoreboard, pull_team_stats
from team_over_under.src.pull_lines import pull_lines

import json

def run_prediction():
    output = predict()
    print(json.dumps(output, indent=4))

def pull_new_data():
    pull_scoreboard()
    pull_team_stats()

def pull_new_lines():
    pull_lines()

if __name__ == "__main__":
    new_data = input("Would you like to pull new data? (y/n) ")
    if new_data.lower() == "y":
        pull_new_data()

    run_prediction()
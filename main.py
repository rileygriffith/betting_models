from team_over_under.predict import predict
from team_over_under.src.pull_data import pull_scoreboard, pull_team_stats
from team_over_under.src.pull_lines import pull_lines

import json

from colorama import Fore, Back, Style

def run_prediction():
    output = predict()
    results_1h, results_total = [], []
    away_team = None
    for key, value in output.items():
        print(Back.GREEN + f'Predictions for {key}:' + Style.RESET_ALL)
        print(Back.CYAN + 'First Half' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 50 Games: {round(value["1H_50"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 20 Games: {round(value["1H_20"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 10 Games: {round(value["1H_10"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 5 Games: {round(value["1H_5"], 1)}' + Style.RESET_ALL)
        results_1h += [round(value["1H_50"], 1), round(value["1H_20"], 1), round(value["1H_10"], 1), round(value["1H_5"], 1)]
        
        print(Back.CYAN + 'Total' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 50 Games: {round(value["T_50"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 20 Games: {round(value["T_20"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 10 Games: {round(value["T_10"], 1)}' + Style.RESET_ALL)
        print(f'\t' + Back.BLACK + f'Trend of last 5 Games: {round(value["T_5"], 1)}' + Style.RESET_ALL)
        results_total += [round(value["T_50"], 1), round(value["T_20"], 1), round(value["T_10"], 1), round(value["T_5"], 1)]

        # Figure out winners and losers of each category
        if len(results_1h) >= 8 or len(results_total) >= 8:
            # Split up arrays
            away_1h = results_1h[:len(results_1h)//2]
            away_total = results_total[:len(results_total)//2]
            home_1h = results_1h[len(results_1h)//2:]
            home_total = results_total[len(results_total)//2:]
            away_categories_won, home_categories_won = 0, 0
            for i in range(len(away_1h)):
                if away_1h[i] > home_1h[i]:
                    away_categories_won += 1
                else:
                    home_categories_won += 1
                if away_total[i] > home_total[i]:
                    away_categories_won += 1
                else:
                    home_categories_won += 1
            results_1h, results_total = [], []

            # Output overall predicted winner
            if home_categories_won > away_categories_won:
                print(Back.RED + f"{key} wins in {home_categories_won} out of 8 model predictions" + Style.RESET_ALL)
                margin = round((sum(home_1h) / len(home_1h)) - (sum(away_1h) / len(away_1h)), 1)
                print(Back.GREEN + f"Average Margin of Victory First Half: {margin}" + Style.RESET_ALL)
                margin = round((sum(home_total) / len(home_total)) - (sum(away_total) / len(away_total)), 1)
                print(Back.GREEN + f"Average Margin of Victory Total: {margin}" + Style.RESET_ALL)
            elif home_categories_won < away_categories_won:
                print(Back.GREEN + f"{away_team} wins in {away_categories_won} out of 8 model predictions" + Style.RESET_ALL)
                margin = round((sum(away_1h) / len(away_1h)) - (sum(home_1h) / len(home_1h)), 1)
                print(Back.GREEN + f"Average Margin of Victory First Half: {margin}" + Style.RESET_ALL)
                margin = round((sum(away_total) / len(away_total)) - (sum(home_total) / len(home_total)), 1)
                print(Back.GREEN + f"Average Margin of Victory Total: {margin}" + Style.RESET_ALL)
            elif home_categories_won == away_categories_won:
                print(Back.GREEN + f"Both teams tie in categories won: {home_categories_won}" + Style.RESET_ALL)

            # Output average totals
            total = round(sum(home_1h) / len(home_1h), 1) + round(sum(away_1h) / len(away_1h), 1)
            print(Back.GREEN + f"Average First Half Total: {total}" + Style.RESET_ALL)
            total = round(sum(home_total) / len(home_total), 1) + round(sum(away_total) / len(away_total), 1)
            print(Back.GREEN + f"Average Total: {total}" + Style.RESET_ALL)
            print("-----------------------------------")
            print()
        else:
            away_team = key

def pull_new_data():
    pull_scoreboard()
    pull_team_stats()

def pull_new_lines():
    pull_lines()

if __name__ == "__main__":
    # new_data = input("Would you like to pull new data? (y/n) ")
    # if new_data.lower() == "y":
    #     pull_new_data()

    run_prediction()
from team_over_under.predict import predict
from team_over_under.src.pull_data import pull_scoreboard, pull_four_factors
from team_over_under.src.pull_lines import pull_lines

from colorama import Back, Style, Fore

import sys

def run_prediction(tomorrow=False):
    output = predict(tomorrow)
    away_team = None
    for game in zip(*(iter(output.keys()),) * 2):
        away_team = game[0]
        home_team = game[1]
        print(Fore.BLACK + Back.GREEN + f'Predictions for {away_team} @ {home_team}:' + Style.RESET_ALL)
        home_categories_won, away_categories_won = 0, 0
        for scope in [50, 20, 10, 5]:
            index = f"T_{scope}"
            spread = round(abs(output[away_team][index] - output[home_team][index]), 1)
            print(f'\t' + Fore.BLACK + Back.CYAN + f'Prediction Based on Last {scope} Games:' + Style.RESET_ALL)
            if output[away_team][index] > output[home_team][index]:
                print(f'\t' + Back.RED + f"{away_team} -{spread}" + Back.CYAN + Fore.BLACK + f" wins {round(output[away_team][index], 1)} - {round(output[home_team][index], 1)}" + Style.RESET_ALL)
                away_categories_won += 1
            elif output[away_team][index] < output[home_team][index]:
                print(f'\t' + Back.RED + f"{home_team} -{spread}" + Back.CYAN + Fore.BLACK + f" wins {round(output[home_team][index], 1)} - {round(output[away_team][index], 1)}" + Style.RESET_ALL)
                home_categories_won += 1
            else:
                print(f'\t' + Back.RED + f'Tie' + Style.RESET_ALL)
            total = output[away_team][index] + output[home_team][index]
            print(f'\t' + Fore.BLACK + Back.CYAN + f"Total {round(total, 1)}" + Style.RESET_ALL)
            print()
        if away_categories_won > home_categories_won:
            print(Back.RED + f"{away_team} wins in {away_categories_won} out of 4 model predictions" + Style.RESET_ALL)
        elif away_categories_won < home_categories_won:
            print(Back.RED + f"{home_team} wins in {home_categories_won} out of 4 model predictions" + Style.RESET_ALL)
        else:
            print(Fore.BLACK + Back.YELLOW + f"Both teams tie in categories won: {home_categories_won}" + Style.RESET_ALL)
        print("-----------------------------------")
        print()

def pull_new_data(tomorrow):
    pull_scoreboard(tomorrow)
    pull_four_factors()

def pull_new_lines():
    pull_lines()

if __name__ == "__main__":
    if "tomorrow" in sys.argv[1:]:
        tomorrow = True
    else:
        tomorrow = False

    if '-n' in sys.argv[1:]:
        pull_new_data(tomorrow)

    run_prediction(tomorrow)

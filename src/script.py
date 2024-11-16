import sys
import os

# Add the parent directory of 'src' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import csv
from players import get_player_data
from src.league  import get_league_standings,get_user_teams

session = requests.session()

def fetch_data(url):
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}, status code: {response.status_code}")
        return None

def save_csv(filename, headers, rows):
    """Save data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)

def merge_save_df(teams,league):
    df_final = teams.merge(league, on='team_id', how='left')
    file_path = 'Data/teams_players.csv'
    df_final.to_csv(file_path, index=False) 

def main():
    print('Data Script started')

    # Fetch and save league standings
    print('Completed league standings fetch')
    league  = get_league_standings()

    # Fetch and save player data
    players = get_player_data()
    print('Completed player data fetch')

    # Fetch/merge and save user team
    users_teams = get_user_teams(players,league)
    merge_save_df(users_teams,league)
    print('Completed users team fetch')
    
    print('Data Script finished')
    
if __name__ == "__main__":
    main()
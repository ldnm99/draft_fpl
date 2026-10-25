import sys
import os
import pandas as pd

# Add the parent directory of 'src' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from   src.utils import fetch_data,save_csv

# Define URLs
BASE_URL            = "https://draft.premierleague.com/api"

#Our league ID 
LEAGUE_ID           = '70113'

#Endpoint to get league data info like standings
LEAGUE_DETAILS_URL  = f"{BASE_URL}/league/"f"{LEAGUE_ID}/details"

#Endpoint to get the managers teams for each gameweek
TEAMS_URL           = f"{BASE_URL}/entry/"

#Endpoint to get the current gameweek
GAME_STATUS_URL     = f"{BASE_URL}/game"

#Player data from the gameweek endpoint
GW_URL              = f"{BASE_URL}/event/"

#Player data endpoint
PLAYER_DATA_URL     = f"{BASE_URL}/bootstrap-static"

#Gets the current league standings and saves into a CSV file  called league_standings.csv in data folder
def get_league_standings():
    """
    Fetches the league standings data, processes it, and saves it to a CSV file.

    This function performs the following steps:
    1. Fetches the league data from a specified URL.
    2. Extracts the standings information from the fetched data.
    3. Processes the standings data to extract relevant fields.
    4. Saves the processed standings data to a CSV file.
    5. Returns the standings data as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the league standings with columns:
                      ['manager_id', 'ID', 'First Name', 'Last Name', 'short_name', 'waiver_pick', 'Team Name']
    """
    data = fetch_data(LEAGUE_DETAILS_URL.format(league_id=LEAGUE_ID))
    if data:
        standings = data.get('league_entries', [])
        standings_data = [
            [entry['entry_id'],
             entry['id'], 
             entry['player_first_name'],
             entry['player_last_name'],
             entry['short_name'],
             entry['waiver_pick'],
             entry['entry_name']]
            for entry in standings
        ]
        headers = ['manager_id', 'ID','First Name', 'Last Name','short_name','waiver_pick','Team Name']
        save_csv('docs/Data/league_standings.csv', headers, standings_data)

#Gets all the players data and saves into a CSV file called players_data.csv in data folder
def get_player_data():

    data = fetch_data(PLAYER_DATA_URL)
    
    if data:
        players = data.get('elements', [])
        player_data = [
            [player['id'], player['first_name'], player['second_name'], player['team'], player['element_type'],
             player['assists'],player['bonus'],  player['total_points'],player['expected_assists'],   player['clean_sheets'],
             player['goals_conceded'], player['goals_scored'], player['minutes'], player['red_cards'],player['starts'],
             player['expected_goals'],player['expected_goal_involvements'], player['expected_goals_conceded'],
             player['code'], player['points_per_game']]
            for player in players
        ]
        headers = ['ID', 'First Name', 'Last Name', 'Team', 'Position', 'Assists', 'bonus', 'Total points', 'xA', 'CS', 'Gc', 'Goals Scored', 'minutes',
                   'red_cards', 'starts', 'xG', 'xGi','xGc','code','PpG']
        save_csv('docs/Data/players_data.csv', headers, player_data)
        print("Player data successfully retrieved.")
        return pd.DataFrame(columns=headers,data=player_data) 

def main():
    """
    Main function to execute the data processing script.
    This function performs the following steps:
    1. Prints the start message.
    2. Fetches league standings data with managers' information.
    3. Fetches player data.
    4. Prints the completion message.
    """

    print("Starting data extraction script...")
    print('----------------------------------------------------------------------')

    # Fetch and save league standings data with just managers' information
    print("Fetching league standings data...")
    get_league_standings()
    print('----------------------------------------------------------------------')
    get_player_data()
    print('----------------------------------------------------------------------')
    print("Data extraction from endpoints script completed successfully.")

# Main function
if __name__ == "__main__":
    main()
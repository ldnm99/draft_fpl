import sys
import os
import pandas as pd

# Add the parent directory of 'src' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from   src.utils import fetch_data

# Define URLs
BASE_URL        = "https://draft.premierleague.com/api"

#Endpoint to get the current gameweek
GAME_STATUS_URL = f"{BASE_URL}/game"

#Player data from the gameweek endpoint
GW_URL      = f"{BASE_URL}/event/"

#Endpoint to get the managers teams for each gameweek
TEAMS_URL   = f"{BASE_URL}/entry/"

#Player/League data csv files
LEAGUE_DATA = pd.read_csv('docs/Data/league_standings.csv')
PLAYER_DATA = pd.read_csv('docs/Data/players_data.csv')

#Path to save the user teams data
USER_TEAMS_PATH  = 'docs/Data/teams_players.csv'

#Gets all the players data from a gameweek and returns a dataframe
def get_player_gw_data(gameweek):
    records = []
    data = fetch_data(GW_URL + str(gameweek) + "/live")
    
    for player_id, value in data['elements'].items():
        stats             = value['stats']
        stats['ID']       = player_id       # Add player ID to stats
        stats['gameweek'] = gameweek        # Add gameweek number
        records.append(stats)

    df = pd.DataFrame(records)
    return df

#Returns the teams of each league member for each gameweek and saves into a CSV file
def get_user_teams(players, managers_ids):
    """
    Retrieves and processes the teams of all managers in a given league for each gameweek up to the current gameweek.

    Args:
        players (pd.DataFrame): DataFrame containing player details with at least an 'ID' column.
        managers_ids (list)   : List of manager IDs.

    Returns:
        pd.DataFrame: A DataFrame containing detailed information about each player's performance in each manager's team across all gameweeks, including their team position and manager ID.
    """

    all_players_data  = []
    current_gameweek = current_gameweek = fetch_data(GAME_STATUS_URL)['current_event']

    #Iterates through every gameweek
    for gameweek in range(1, current_gameweek + 1):
        # All players for a specific gameweek
        gwplayers       = get_player_gw_data(gameweek)
        gwplayers['ID'] = gwplayers['ID'].astype(str)

        #Iterates through every manager
        for manager_id in managers_ids:
            team = fetch_data(f"{TEAMS_URL}{manager_id}/event/{gameweek}")

            # Get all players of a manager for a specific gameweek
            teamplayers             = pd.DataFrame(team['picks']).rename(columns={'element': 'ID', 'position': 'team_position'})
            teamplayers['ID']       = teamplayers['ID'].astype(str)
            teamplayers['gameweek'] = gameweek
            
            # Filter gameweek players to only those in the manager's team
            manager_gwplayers = pd.merge(gwplayers, teamplayers[['ID']], on='ID', how='inner')

            # Merge with player details
            player_data       = pd.merge(players, manager_gwplayers, on='ID', how='inner')

            # Merge with team positions
            player_data = pd.merge(
                player_data, 
                teamplayers[['ID', 'team_position', 'gameweek']], 
                on='ID', 
                how='left'
            )
            player_data['manager_id'] = manager_id

            all_players_data.append(player_data)

    final_df = pd.concat(all_players_data, ignore_index=True)

    # Remove any duplicate gameweek columns and keep only one
    final_df = final_df.loc[:, ~final_df.columns.str.contains('^gameweek')]
    final_df['gameweek'] = gameweek

    return final_df

def main():
    # Processing steps for user team data
    print("Starting data processing script...")
    print('----------------------------------------------------------------------')
    managers_ids  = LEAGUE_DATA['manager_id']
    players       = PLAYER_DATA[['ID', 'First Name', 'Last Name', 'Team', 'Position']].copy()
    players['ID'] = players['ID'].astype(str)
    
    users_teams   = get_user_teams(players, managers_ids)

    # Merge and save the user team data
    merged_data    = users_teams.merge(LEAGUE_DATA, on='manager_id', how='left')
    merged_data.to_csv(USER_TEAMS_PATH, index=False) 

    print("User team data successfully processed and saved to .CSV file.")

# Main function
if __name__ == "__main__":
    main()
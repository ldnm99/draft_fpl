import pandas as pd
from src.utils import fetch_data,save_csv
"""
This module provides functions to interact with the Fantasy Premier League (FPL) API to fetch league standings and user teams data.

Functions:
    get_league_standings():
        Fetches the current league standings and saves the data into a CSV file.
        Returns a pandas DataFrame containing the league standings.

    get_user_teams(players, managers_ids):
        Fetches the teams of each league member for each gameweek and saves the data into a CSV file.
        Args:
            players (pd.DataFrame): DataFrame containing player information.
            managers_ids (list): List of manager IDs.
        Returns:
            pd.DataFrame: DataFrame containing the teams of each league member for each gameweek.
"""

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

#Gets all the players data from a gameweek and returns a dataframe
def get_player_gw_data(gameweek):
    records = []
    data = fetch_data(GW_URL + str(gameweek) + "/live")
    
    for player_id, value in data['elements'].items():
        stats = value['stats']
        stats['ID'] = player_id  # Add player ID to stats
        stats['gameweek'] = gameweek  # Add gameweek number
        records.append(stats)
    df = pd.DataFrame(records)
    return df

#Returns the current league standings and saves into a CSV file
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
        return pd.DataFrame(columns=headers,data=standings_data)

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

# Function to calculate league classification
def league_classification(df_final):
    
    # Filter players by teams with positions less than 12
    filtered_df = df_final[df_final['team_position'] < 12]
    
    # Group by team and gameweek, then sum points for each gameweek
    grouped = (
        filtered_df.groupby(['Team Name', 'gameweek'])['total_points']
        .sum()
        .reset_index()
    )
    
    # Calculate cumulative points for each team
    grouped['cumulative_points'] = grouped.groupby('Team Name')['total_points'].cumsum()
    
    # Get the latest cumulative points for each team
    result_df         = grouped.groupby('Team Name')['cumulative_points'].max().reset_index()
    result_df.columns = ['Equipa', 'Pontos']
    result_df         = result_df.sort_values(by=['Pontos'], ascending=False).reset_index(drop=True)
    print("League standings classification successfully generated.")
    return result_df
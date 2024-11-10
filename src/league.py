import pandas as pd
from src.players import get_player_gw_data

BASE_URL            = "https://draft.premierleague.com/api"

#Our league ID 
LEAGUE_ID           = '70113'

#Endpoint to get league data info like standings
LEAGUE_DETAILS_URL  = f"{BASE_URL}/league/"f"{LEAGUE_ID}/details"

#Endpoint to get the managers teams for each gameweek
TEAMS_URL           = f"{BASE_URL}/entry/"

#Endpoint to get the current gameweek
GAME_STATUS_URL     = f"{BASE_URL}/game"

#Returns the number of the current gameweek 
def get_current_gw():
    from src.script import fetch_data
    data = fetch_data(GAME_STATUS_URL)
    current_gameweek = data['current_event']
    return current_gameweek

#Returns the current league standings and saves into a CSV file
def get_league_standings():
    from src.script import fetch_data
    from src.script import save_csv
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
        headers = ['team_id', 'ID','First Name', 'Last Name','short_name','waiver_pick','Team Name']
        save_csv('Data/league_standings.csv', headers, standings_data)
        return pd.DataFrame(columns=headers,data=standings_data)
    
#Returns the teams of each league member for each gameweek and saves into a CSV file
def get_user_teams(players, league):
    from src.script import fetch_data
    
    ids = league['team_id']

    all_player_data = []
    current_gameweek = get_current_gw()

    #Iterates through every gameweek
    for gameweek in range(1, current_gameweek + 1):
        gwplayers = get_player_gw_data(gameweek)
        for id in ids:
            team = fetch_data(TEAMS_URL+str(id)+"/event/"+str(gameweek))
            
            teamplayers = pd.DataFrame(team['picks'])
           
            teamplayers.rename(columns={'element': 'ID'}, inplace=True)
            teamplayers['ID'] = teamplayers['ID'].astype(str)
            teamplayers['gameweek'] = gameweek
            team_ids = teamplayers['ID'].tolist()
            teamplayers.rename(columns={'position': 'team_position'}, inplace=True)
            
            players = players.copy()
            players['ID'] = players['ID'].astype(str)
            players = players[['ID', 'First Name', 'Last Name', 'Team','Position']]

            gwplayers['ID'] = gwplayers['ID'].astype(str)
            merged_df = pd.merge(players, gwplayers, left_on='ID', right_on='ID', how='inner')
            
            df_merged = pd.merge(merged_df, teamplayers[['ID', 'team_position', 'gameweek']], on=['ID', 'gameweek'], how='left')

            filtered_df = df_merged[df_merged['ID'].isin(team_ids)].copy() 
            filtered_df['team_id'] = id
            all_player_data.append(filtered_df) 
    final_df = pd.concat(all_player_data, ignore_index=True)
    return final_df


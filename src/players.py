import pandas as pd
from src.utils import fetch_data,save_csv

# Define URLs
BASE_URL            = "https://draft.premierleague.com/api"

#Player data endpoint
PLAYER_DATA_URL     = f"{BASE_URL}/bootstrap-static"

#Gets all the players data and saves it into data folder
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
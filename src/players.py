import pandas as pd

# Define URLs
BASE_URL            = "https://draft.premierleague.com/api"

#Player data endpoint
PLAYER_DATA_URL     = f"{BASE_URL}/bootstrap-static"

#Player data from a gameweek endpoint
GW_URL              = f"{BASE_URL}/event/"

#Gets all the players data and saves it into data folder
def get_player_data():
    from script import fetch_data
    from script import save_csv
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
        save_csv('Data/players_data.csv', headers, player_data)
        return pd.DataFrame(columns=headers,data=player_data)

#Gets all the players data from a gameweek and returns a dataframe
def get_player_gw_data(gameweek):
    from script import fetch_data
    data = fetch_data(GW_URL + str(gameweek) + "/live")
    records = []
    for player_id, value in data['elements'].items():
        stats = value['stats']
        stats['ID'] = player_id  # Add player ID to stats
        stats['gameweek'] = gameweek  # Add gameweek number
        records.append(stats)
    df = pd.DataFrame(records)
    return df
       
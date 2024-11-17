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
    file_path = 'docs/Data/teams_players.csv'
    df_final.to_csv(file_path, index=False) 
    return df_final

def create_htmls(standings):
    standings_html = standings.to_html(index =False)
     # Define custom CSS for styling
    custom_css = """
    <style>
        body {
            background-color: black; /* Dark background */
            color: white; /* White text */
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        table {
            width: 60%;
            margin: 20px auto; /* Center the table */
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid white; /* White borders */
            padding: 10px;
            text-align: center; /* Center-align content */
        }
        th {
            background-color: #444; /* Dark grey for headers */
        }
        tbody tr:nth-child(odd) {
            background-color: #222; /* Slightly lighter grey for odd rows */
        }
        tbody tr:nth-child(even) {
            background-color: #333; /* Darker grey for even rows */
        }
    </style>
    """

    # Add a title and inject the CSS into the HTML
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>League Standings</title>
        {custom_css}
    </head>
    <body>
        <h2 style="text-align: center;">Current League Standings</h2>
        {standings_html}
    </body>
    </html>
    """
    with open('docs/league_standings.html', 'w') as f:
        f.write(full_html)

def league_standings(df_final):
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
    result_df = grouped.groupby('Team Name')['cumulative_points'].max().reset_index()
    result_df.columns = ['Equipa', 'Pontos']
    result_df = result_df.sort_values(by=['Pontos'], ascending=False).reset_index(drop=True)
    return result_df



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
    final_df = merge_save_df(users_teams,league)
    print('Completed users team fetch')
    
    print('Data Script finished')

    standings = league_standings(final_df)
    create_htmls(standings)


    
if __name__ == "__main__":
    main()
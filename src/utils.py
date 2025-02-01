import sys
import os

# Add the parent directory of 'src' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import csv

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
    df_final = teams.merge(league, on='manager_id', how='left')
    file_path = 'docs/Data/teams_players.csv'
    df_final.to_csv(file_path, index=False) 
    print("User team data successfully processed and saved.")
    return df_final
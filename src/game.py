import requests
import csv
import pandas as pd
import endpoints
from .endpoints import API_ENDPOINTS


def fetch_data(url):
    response = requests.get(url)
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

def main():
    league_id = '70113'
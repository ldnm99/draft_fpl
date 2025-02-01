import sys
import os

# Add the parent directory of 'src' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from players     import get_player_data
from league      import get_league_standings, get_user_teams, league_classification
from utils       import merge_save_df
from visuals     import create_standings_html, create_visuals, create_cumulative_html

"""
This script processes and generates HTML reports for league standings and player data.

Modules:
    sys: Provides access to some variables used or maintained by the interpreter.
    os: Provides a way of using operating system dependent functionality like reading or writing to the file system.
    players: Custom module to fetch player data.
    league: Custom module to fetch league standings, user teams, and generate league classification.
    utils: Custom module to merge and save DataFrame.
    visuals: Custom module to create HTML reports and visualizations.

Functions:
    main():
        Main function to execute the data processing script.
"""

def main():
    """
    Main function to execute the data processing script.
    This function performs the following steps:
    1. Prints the start message.
    2. Fetches league standings data with managers' information.
    3. Fetches player data.
    4. Fetches user team data, merges it with league standings, and saves the result.
    5. Generates league standings classification.
    6. Creates HTML reports.
    7. Prints the completion message.
    """

    print("Starting data processing script...")
    print('----------------------------------------------------------------------')

    # Fetch and save league standings data with just managers' information
    print("Fetching league standings data...")
    league_standings = get_league_standings()
    print('----------------------------------------------------------------------')

    # Fetch and save player data
    print("Fetching player data...")
    players = get_player_data()
    print('----------------------------------------------------------------------')

    # Processing steps for user team data
    players       = players[['ID', 'First Name', 'Last Name', 'Team', 'Position']].copy()
    players['ID'] = players['ID'].astype(str)
    managers_ids  = league_standings['manager_id']
    
    print("Fetching user team data and merging with league standings...")
    users_teams = get_user_teams(players, managers_ids)
    final_df    = merge_save_df(users_teams, league_standings)
    print('----------------------------------------------------------------------')

    print("Generating league standings classification...")
    standings = league_classification(final_df)
    print('----------------------------------------------------------------------')

    print("Creating HTML reports...")
    create_standings_html(standings)
    print('----------------------------------------------------------------------')

    print("Data processing script completed successfully.")

if __name__ == "__main__":
    main()
import pandas as pd

TEAM_PLAYERS_DATA = pd.read_csv('docs/Data/teams_players.csv')

# Function to calculate league classification
def main():
    
    # Filter players by teams with positions less than 12 (starting 11)
    players_on = TEAM_PLAYERS_DATA[TEAM_PLAYERS_DATA['team_position'] < 12]
    
    # Group by team and gameweek, then sum points for each gameweek
    grouped = (
        players_on.groupby(['Team Name', 'gameweek'])['total_points']
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
    result_df.to_html('docs/Graphs/league_standings.html', index=False)
    print("HTML report successfully generated.")

# Main function
if __name__ == "__main__":
    main()

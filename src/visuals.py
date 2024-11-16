import pandas as pd
import plotly.express as px

DATA = {}

def create_visuals():
    DATA = pd.read_csv('docs/Data/teams_players.csv')
    DATA['Cumulative Points'] = DATA.groupby('team_id')['total_points'].cumsum()

    fig_league = px.line(
    DATA,
    x='gameweek',
    y='Cumulative Points',
    color='Team Name',
    title="Cumulative Points by Gameweek for Each Team",
    labels={'gameweek': 'Gameweek', 'Cumulative Points': 'Cumulative Points'},
    hover_name='Team Name'
    )
    fig_league.write_html("docs/Graphs/cumulative_points_chart.html")

def main():
    create_visuals()    
    
if __name__ == "__main__":
    main()
    
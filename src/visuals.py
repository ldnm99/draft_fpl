import pandas as pd
import plotly.express as px

DATA = {}

def create_visuals():
    DATA = pd.read_csv('docs/Data/teams_players.csv')
    DATA = DATA.sort_values(by=['team_id', 'gameweek'])
    players_played = DATA[DATA['team_position'] < 12]
    result = players_played.groupby(['gameweek', 'Team Name'])['total_points'].sum().reset_index()

    fig_league = px.line(
    result,
    x='gameweek',
    y='total_points',
    color='Team Name',
    labels={'gameweek': 'Gameweek', 'total_points': 'Points'},
    hover_name='Team Name',
    line_shape='linear'
    )
    # Customize the tooltip template
    fig_league.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                  "Gameweek: %{x}<br>" +
                  "Points: %{y}<br>" +
                  "<extra></extra>"
    )
    fig_league.write_html("docs/Graphs/cumulative_points_chart.html")

def main():
    create_visuals()    
    
if __name__ == "__main__":
    main()
    
import pandas as pd
import plotly.express as px

TEAM_PLAYERS_DATA = pd.read_csv('docs/Data/teams_players.csv')

def create_visuals():
    DATA = TEAM_PLAYERS_DATA.sort_values(by=['team_id', 'gameweek'])
    players_played = DATA[DATA['team_position'] < 12]
    result = players_played.groupby(['gameweek', 'Team Name'])['total_points'].sum().reset_index()

    fig_league = px.line(
        result,
        x          = 'gameweek',
        y          = 'total_points',
        color      = 'Team Name',
        labels     = {'gameweek': 'Gameweek', 'total_points': 'Points'},
        hover_name = 'Team Name',
        line_shape = 'linear'
    )
    # Customize the tooltip template
    fig_league.update_traces(
        hovertemplate = "<b>%{hovertext}</b><br><br>" +
                  "Gameweek: %{x}<br>" +
                  "Points: %{y}<br>" +
                  "<extra></extra>"
    )
    fig_league.write_html("docs/Graphs/gameweek_points_chart.html")
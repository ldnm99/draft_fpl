import pandas as pd
import plotly.express as px

DATA = {}

# for points per gameweek
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
    fig_league.write_html("docs/Graphs/gameweek_points_chart.html")


# for cumulative points per gameweek
def create_visuals2():
    # Load the data
    DATA = pd.read_csv('docs/Data/teams_players.csv')

    # Filter players with team_position < 12
    players_played = DATA[DATA['team_position'] < 12].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Calculate cumulative points
    team_points_per_gameweek = players_played.groupby(['Team Name', 'gameweek'])['total_points'].sum().reset_index()

    # Calculate cumulative points for each team
    team_points_per_gameweek['cumulative_points'] = team_points_per_gameweek.groupby('Team Name')['total_points'].cumsum()

    # Sort the DataFrame for better readability
    sorted_df = team_points_per_gameweek.sort_values(by=['gameweek', 'Team Name'])

    # Create the line chart
    fig_league = px.line(
        sorted_df,
        x='gameweek',
        y='cumulative_points',  # Use cumulative_points for visualization
        color='Team Name',
        labels={'gameweek': 'Gameweek', 'cumulative_points': 'Cumulative Points'},
        hover_name='Team Name',
        line_shape='linear'
    )

    # Customize the tooltip template
    fig_league.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                      "Gameweek: %{x}<br>" +
                      "Cumulative Points: %{y}<br>" +
                      "<extra></extra>"
    )
    
    # Save the chart as an HTML file
    fig_league.write_html("docs/Graphs/cumulative_points_chart.html")

def main():
    create_visuals()    
    create_visuals2()  
    
if __name__ == "__main__":
    main()
    
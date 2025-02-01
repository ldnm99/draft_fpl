import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

DATA = {}

def create_standings_html(standings):
    """Generates an HTML file from the given standings DataFrame with custom CSS styling.
    Args:
        standings (pandas.DataFrame): A DataFrame containing the standings data to be converted to HTML.
    Returns:
        None: The function writes the generated HTML to a file and does not return any value.
    The generated HTML file is saved to 'docs/Graphs/league_standings.html' and includes custom CSS for styling the table.
    """

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

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {custom_css}
    </head>
    <body>
        {standings_html}
    </body>
    </html>
    """
    with open('docs/Graphs/league_standings.html', 'w') as f:
        f.write(full_html)
    print("HTML reports successfully generated.")

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
    return sorted_df

def create_cumulative_html(sorted_df): 
    # Create traces for each team 
    traces = [] 
    visibility_flags = {}

    for team in sorted_df['Team Name'].unique(): 
        team_data = sorted_df[sorted_df['Team Name'] == team] 
        traces.append(go.Scatter( x=team_data['gameweek'],
                                 y=team_data['cumulative_points'], 
                                 mode='lines', 
                                 name=team, 
                                 visible=True )) 
        visibility_flags[team] = True
        
    # Create buttons for multi-select functionality
    buttons = []
    for i, team in enumerate(sorted_df['Team Name'].unique()):
        buttons.append(dict(
            label=team,
            method='update',
            args=[{'visible': [team == trace.name or visibility_flags[trace.name] for trace in traces]},
                  {'showlegend': True}],
            execute=True
        ))

    # Add "Show All" and "Hide All" buttons
    buttons.append(dict(
        label='Show All',
        method='update',
        args=[{'visible': [True] * len(traces)},
              {'showlegend': True}]
    ))

    buttons.append(dict(
        label='Hide All',
        method='update',
        args=[{'visible': [False] * len(traces)},
              {'showlegend': True}]
    ))

    # Create the figure
    fig_league = go.Figure(data=traces)
    fig_league.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                showactive=True,
                buttons=buttons,
                x=1.05,
                y=1.2
            ),
            dict(
                type="buttons",
                direction="right",
                showactive=False,
                x=1.05,
                y=1,
                buttons=[dict(
                    label='Autoscale',
                    method='relayout',
                    args=[{
                        'xaxis.autorange': True,
                        'yaxis.autorange': True
                    }]
                )]
            )
        ],
        showlegend=True,
        title='Cumulative Points by Team',
        xaxis_title='Gameweek',
        yaxis_title='Cumulative Points',
        xaxis=dict(
            tickmode='array',
            tickvals=list(sorted_df['gameweek'].unique()),
            rangeslider=dict(
                visible=True
            ),
            type='linear'
        ),
        autosize=True,
    )

    def update_visibility_flags(event): 
        # Update visibility_flags based on current trace visibility 
        for trace in traces: 
            visibility_flags[trace.name] = trace.visible

    # Attach the update_visibility_flags function to be called on click event
    #fig_league.on_click(update_visibility_flags)

    # Save the chart as an HTML file
    #fig_league.write_html("docs/Graphs/cumulative_points_chart.html")
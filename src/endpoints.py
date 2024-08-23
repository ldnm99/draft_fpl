API_ENDPOINT = "https://draft.fantasy.premierleague.com/api/" 

API_ENDPOINTS = {
    'game':'{}game/'.format(API_ENDPOINT),
    'dynamic': "{}bootstrap-dynamic/".format(API_ENDPOINT),
    "static": "{}bootstrap-static/".format(API_ENDPOINT),

    'details':'{}league/70113/details/'.format(API_ENDPOINT),
    'element':'{}league/70113/element-status/'.format(API_ENDPOINT),
    'trades' :'{}league/70113/trades/'.format(API_ENDPOINT),
    'status' :'{}pl/event-status/'.format(API_ENDPOINT),
    'transactions' :'{}league/70113/transactions/'.format(API_ENDPOINT),
    

    "fixtures": "{}fixtures/".format(API_ENDPOINT),
    "gameweeks": "{}events/".format(API_ENDPOINT),
    "gameweek_fixtures": "{}fixtures/?event={{}}".format(API_ENDPOINT),
    "gameweek_live": "{}event/{{}}/live".format(API_ENDPOINT),
    "league_classic": "{}leagues-classic/{{}}/standings/".format(API_ENDPOINT),
    "players": "{}elements/".format(API_ENDPOINT),
    "player": "{}element-summary/{{}}/".format(API_ENDPOINT),
    "settings": "{}game-settings/".format(API_ENDPOINT),
}

PICKS_FORMAT = "{} {}{}"
MYTEAM_FORMAT = "{}{}"

LEAGUE_ID = 70113

MIN_GAMEWEEK = 1
MAX_GAMEWEEK = 47
API_BASE_URL = "https://draft.fantasy.premierleague.com/api/" 

API_URLS = {
    'game':'{}game/'.format(API_BASE_URL),
    'dynamic': "{}bootstrap-dynamic/".format(API_BASE_URL),
    "static": "{}bootstrap-static/".format(API_BASE_URL),

    'details':'{}league/70113/details/'.format(API_BASE_URL),
    'element':'{}league/70113/element-status/'.format(API_BASE_URL),
    'trades' :'{}league/70113/trades/'.format(API_BASE_URL),
    'status' :'{}pl/event-status/'.format(API_BASE_URL),
    'transactions' :'{}league/70113/transactions/'.format(API_BASE_URL),
    

    "fixtures": "{}fixtures/".format(API_BASE_URL),
    "gameweeks": "{}events/".format(API_BASE_URL),
    "gameweek_fixtures": "{}fixtures/?event={{}}".format(API_BASE_URL),
    "gameweek_live": "{}event/{{}}/live".format(API_BASE_URL),
    "league_classic": "{}leagues-classic/{{}}/standings/".format(API_BASE_URL),
    "players": "{}elements/".format(API_BASE_URL),
    "player": "{}element-summary/{{}}/".format(API_BASE_URL),
    "settings": "{}game-settings/".format(API_BASE_URL),
}

PICKS_FORMAT = "{} {}{}"
MYTEAM_FORMAT = "{}{}"

LEAGUE_ID = 70113

MIN_GAMEWEEK = 1
MAX_GAMEWEEK = 47
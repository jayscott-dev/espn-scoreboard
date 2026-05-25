import requests
import json
from nba.scoreboard import NBAScoreboard
from mlb.scoreboard import MLBScoreboard

SUPPORTED_LEAGUES = [
    "nba",
    "mlb",
]

NBA_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
MLB_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

def fetch_nba_scoreboard(date: str | None = None) -> dict:
    params = {}
    if date:
        params["dates"] = date
    resp = requests.get(
        NBA_URL,
        headers = {"User-Agent": "nba-scores-learning-script/1.0"},
        params = params,
        timeout = 10,
    )
    resp.raise_for_status()
    return resp.json()

def fetch_mlb_scoreboard(date: str | None = None) -> dict:
    params = {}
    if date:
        params["dates"] = date
    resp = requests.get(
        MLB_URL,
        headers = {"User-Agent": "mlb-scores-learning-script/1.0"},
        params = params,
        timeout = 10,
    )
    resp.raise_for_status()
    return resp.json()

def write_scoreboard_data(data: dict, league: str):
    with open(f"../data/{league}_scoreboard.json", "w") as file:
        json.dump(data, file, indent = 4)

def fetch_espn_data (league: str, write_data: bool, date: str | None = None):
    data = {}
    match league:
        case "nba":
            data = fetch_nba_scoreboard(date)
            scoreboard = NBAScoreboard.from_dict(data)
            scoreboard.print_games()
        case "mlb":
            data = fetch_mlb_scoreboard(date)
            scoreboard = MLBScoreboard.from_dict(data)
            scoreboard.print_games()
        case _:
            print("Not yet implemented")

    if data and write_data:
        write_scoreboard_data(data, league)

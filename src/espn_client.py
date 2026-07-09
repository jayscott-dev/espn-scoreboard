import requests
import json
from dataclasses import dataclass
from nba.scoreboard import NBAScoreboard
from mlb.scoreboard import MLBScoreboard
from wnba.scoreboard import WNBAScoreboard
from fifa.scoreboard import FIFAScoreboard

SUPPORTED_LEAGUES = [
    "nba",
    "mlb",
    "wnba",
    "fifa",
]

NBA_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
MLB_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
WNBA_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"
FIFA_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

@dataclass
class ClientConfig:
    league: str
    write_data: bool
    date: str | None = None

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

def fetch_wnba_scoreboard(date: str | None = None) -> dict:
    params = {}
    if date:
        params["dates"] = date
    resp = requests.get(
        WNBA_URL,
        headers = {"User-Agent": "wnba-scores-learning-script/1.0"},
        params = params,
        timeout = 10,
    )
    resp.raise_for_status()
    return resp.json()

def fetch_fifa_scoreboard(date: str | None = None) -> dict:
    params = {}
    if date:
        params["date"] = date
    resp = requests.get(
        FIFA_URL,
        headers = {"User-Agent": "fifa-scores-learning-script/1.0"},
        params = params,
        timeout = 10,
    )
    resp.raise_for_status()
    return resp.json()

def write_scoreboard_data(data, league: str):
    with open(f"../data/{league}_scoreboard.json", "w") as file:
        json.dump(data, file, indent = 4)

def fetch_espn_data(league: str, date: str | None = None):
    match league:
        case "nba":
            return NBAScoreboard.from_dict(fetch_nba_scoreboard(date))
        case "mlb":
            return MLBScoreboard.from_dict(fetch_mlb_scoreboard(date))
        case "wnba":
            return WNBAScoreboard.from_dict(fetch_wnba_scoreboard(date))
        case "fifa":
            return FIFAScoreboard.from_dict(fetch_fifa_scoreboard(date))

def print_espn_data (client_config: ClientConfig):
    data = fetch_espn_data(client_config.league, client_config.date)

    if not data:
        print("Not yet implemented")
    else:
        data.print_games()

    if data and client_config.write_data:
        write_scoreboard_data(data, client_config.league)

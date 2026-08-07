import requests
import json
from dataclasses import dataclass
from config import settings
from nba.scoreboard import NBAScoreboard
from mlb.scoreboard import MLBScoreboard
from wnba.scoreboard import WNBAScoreboard
from fifa.scoreboard import FIFAScoreboard
from exceptions import NotYetImplementedError, UnsupportedLeagueError

SUPPORTED_LEAGUES = [
    "nba",
    "mlb",
    "wnba",
    "fifa",
    "tennis",
]

NBA_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
MLB_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
WNBA_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"
FIFA_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

HEADERS = {
    "User-Agent": settings.espn_user_agent,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "application/json"
}

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
        headers = HEADERS,
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
        headers = HEADERS,
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
        headers = HEADERS,
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
        headers = HEADERS,
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
        case _:
            if league in SUPPORTED_LEAGUES:
                raise NotYetImplementedError(f"Scoreboard for league {league} is not yet implemented")
            else:
                raise UnsupportedLeagueError(f"League {league} is not supported")

def print_espn_data (client_config: ClientConfig):
    try:
        data = fetch_espn_data(client_config.league, client_config.date)
        data.print_games()
        if client_config.write_data:
            write_scoreboard_data(data, client_config.league)
    except NotYetImplementedError:
        print("Not yet implemented")
    except UnsupportedLeagueError:
        print("League not supported")

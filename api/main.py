import os 
import src.espn_client as ec
import serializers as srl
from exceptions import NotYetImplementedError, UnsupportedLeagueError

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScoreboardResponse, LeagueResponse, ConfigResponse

app = FastAPI()
allowed_origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ["GET"],
    allow_headers = ["*"],
)

@app.get("/leagues")
def get_leagues() -> LeagueResponse:
    return LeagueResponse (leagues = ec.SUPPORTED_LEAGUES)

@app.get("/config")
def get_config() -> ConfigResponse:
    return ConfigResponse (poll_interval_ms = int(os.getenv("POLL_INTERVAL_MS", "120000")))

@app.get("/scoreboard")
def get_scoreboard(
    league: str = Query(..., description = "League to fetch", examples = ["nba"]),
    date: str | None = Query(None, description = "Date in YYYYMMDD format"),
) -> ScoreboardResponse:
    try:
        scoreboard = ec.fetch_espn_data(league, date)
        return srl.scoreboard_response_from(scoreboard)
    except NotYetImplementedError as exc:
        raise HTTPException(status_code = 400, detail = str(exc))
    except UnsupportedLeagueError as exc:
        raise HTTPException(status_code = 400, detail = str(exc))

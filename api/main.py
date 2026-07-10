import src.espn_client as ec
import serializers as srl

from fastapi import FastAPI, Query
from models import ScoreboardResponse

app = FastAPI()

@app.get("/leagues")
def get_leagues():
    return {"leagues": ec.SUPPORTED_LEAGUES}

@app.get("/config")
def get_config():
    return {"poll_interval_ms": 120000}

@app.get("/scoreboard")
def get_scoreboard(
    league: str = Query(..., description = "League to fetch", examples = ["nba"]),
    date: str | None = Query(None, description = "Date in YYYYMMDD format"),
) -> ScoreboardResponse:
    scoreboard = ec.fetch_espn_data(league, date)
    if scoreboard:
        return srl.scoreboard_response_from(scoreboard)
    else:
        return ScoreboardResponse(league = "n/a", date_display = "n/a")

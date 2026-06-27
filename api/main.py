import src.espn_client as ec

from fastapi import FastAPI

app = FastAPI()

@app.get("/leagues")
def get_leagues():
    return {"leagues": ec.SUPPORTED_LEAGUES}

@app.get("/config")
def get_config():
    return {"poll_interval_ms": 120000}
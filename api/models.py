from pydantic import BaseModel

class ScoreboardResponse(BaseModel):
    league: str
    date_display: str
    games: list[GameResponse]

class GameResponse(BaseModel):
    title: str
    start_date: str
    start_time: str
    status: str
    status_detail: str
    series_info: str | None
    home_team: TeamResponse
    away_team: TeamResponse

class TeamResponse(BaseModel):
    id: str
    name: str
    score: str
    record: str | None

from pydantic import BaseModel

class ScoreboardResponse(BaseModel):
    league: str
    date_display: str
    games: list[GameResponse]

class GameResponse(BaseModel):
    title: str

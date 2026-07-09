from pydantic import BaseModel

class ScoreboardResponse(BaseModel):
    league: str
    date_display: str

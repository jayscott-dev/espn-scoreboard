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
    stat_leaders: list[StatLeaderResponse]

class TeamResponse(BaseModel):
    id: str
    name: str
    score: str
    record: str | None

class StatLeaderResponse(BaseModel):
    team_id: str
    label: str
    name: str
    stat_value: str

class LeagueResponse(BaseModel):
    leagues: list[str]

class ConfigResponse(BaseModel):
    poll_interval_ms: int

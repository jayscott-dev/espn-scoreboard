from base import Scoreboard
from models import ScoreboardResponse

def scoreboard_response_from(scoreboard: Scoreboard) -> ScoreboardResponse:
    return ScoreboardResponse (
        league = scoreboard.league,
        date_display = scoreboard.date_display
    )

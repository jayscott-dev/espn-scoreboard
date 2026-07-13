from base import Scoreboard, Game
from models import ScoreboardResponse, GameResponse

def scoreboard_response_from(scoreboard: Scoreboard) -> ScoreboardResponse:
    return ScoreboardResponse (
        league = scoreboard.league,
        date_display = scoreboard.date_display,
        games = [game_response_from(game) for game in scoreboard.games]
    )

def game_response_from(game: Game) -> GameResponse:
    return GameResponse (
        title = game.title,
        start_date = game.start_date,
        start_time = game.start_time,
        status = game.status,
        status_detail = game.status_detail,
        series_info = game.series_info,
    )
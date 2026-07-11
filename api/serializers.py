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
        title = game.title
    )
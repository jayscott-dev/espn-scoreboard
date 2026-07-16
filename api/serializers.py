from base import Scoreboard, Game, Team
from models import ScoreboardResponse, GameResponse, TeamResponse

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
        home_team = team_response_from(game.home_team),
        away_team = team_response_from(game.away_team),
    )

def team_response_from(team: Team) -> TeamResponse:
    return TeamResponse (
        id = team.id,
        name = team.name,
        score = team.score,
        record = team.record,
    )

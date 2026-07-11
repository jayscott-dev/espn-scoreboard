from dataclasses import dataclass
from nba.game import NBAGame
import utils.date as date_utils
from base import Scoreboard, Game
from collections.abc import Sequence

@dataclass
class NBAScoreboard(Scoreboard):
    _games: list[NBAGame]

    @classmethod
    def from_dict(cls, data: dict) -> "NBAScoreboard":
        games = [NBAGame.from_dict(event) for event in data.get("events", [])]
        return cls(_games = games)
    
    def print_games(self):
        num_games = len(self.games)
        if num_games == 0:
            print("0 Games Found")
        else:
            print(f"{num_games} Game{'s' if num_games != 1 else ''} {self.date_display}")
        for game in self._games:
            game.print_game_data() 

    @property
    def games(self) -> Sequence[Game]:
        return self._games

    @property
    def league(self) -> str:
        return "NBA"

    @property
    def date_display(self) -> str:
        if len(self._games) > 0:
            d1 = self._games[0].date
            d2 = self._games[-1].date
            return date_utils.display_games_dt(d1, d2)
        else:
            return ""

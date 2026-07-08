from dataclasses import dataclass
from wnba.game import WNBAGame
import utils.date as date_utils
from typing import Self

@dataclass
class WNBAScoreboard:
    games: list[WNBAGame]
    league: str = "WNBA"

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        games = [WNBAGame.from_dict(event) for event in data.get("events", [])]
        return cls(games = games)
    
    def print_games(self):
        num_games = len(self.games)
        if num_games == 0:
            print("0 Games Found")
        else:
            print(f"{num_games} Game{'s' if num_games != 1 else ''} {self.date_display}")
        for game in self.games:
            game.print_game_data() 

    @property
    def date_display(self) -> str:
        if len(self.games) > 0:
            d1 = self.games[0].date
            d2 = self.games[-1].date
            return date_utils.display_games_dt(d1, d2)
        else:
            return ""

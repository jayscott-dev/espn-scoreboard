from dataclasses import dataclass
from nba.game import NBAGame

@dataclass
class NBAScoreboard:
    games: list[NBAGame]

    @classmethod
    def from_dict(cls, data: dict) -> "NBAScoreboard":
        games = [NBAGame.from_dict(event) for event in data.get("events", [])]
        return cls(games = games)
    
    def print_games(self):
        print(f"{len(self.games)} Games Today")
        for game in self.games:
            game.print_game_data() 
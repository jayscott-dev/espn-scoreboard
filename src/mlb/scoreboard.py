from dataclasses import dataclass
from mlb.game import MLBGame

@dataclass
class MLBScoreboard:
    games: list[MLBGame]

    @classmethod
    def from_dict(cls, data: dict) -> "MLBScoreboard":
        games = [MLBGame.from_dict(event) for event in data.get("events", [])]
        return cls(games = games)
    
    def print_games(self):
        num_games = len(self.games)
        print(f"{num_games} Game{'s' if num_games != 1 else ''} Today")
        for game in self.games:
            game.print_game_data() 
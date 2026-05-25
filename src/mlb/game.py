from dataclasses import dataclass
import utils.date as date_utils
from typing import Optional
from mlb.team import MLBTeam

@dataclass
class MLBGame:
    name: str
    date: str
    teams: dict[str, MLBTeam]
    
    @classmethod
    def from_dict(cls, game: dict) -> "MLBGame":
       competitions = game.get("competitions", [])[0]
       
       teams = {}
       for team in competitions.get("competitors", []):
           teams[team["homeAway"]] = MLBTeam.from_dict(team)

       return cls (
           name = game.get("name", ""),
           date = game.get("date", ""),
           teams = teams,
       ) 
    
    def home_team(self) -> MLBTeam:
        return self.teams["home"]
    
    def away_team(self) -> MLBTeam:
        return self.teams["away"]

    def print_game_data(self):
        print(f"\n{game_title(self)}")
        print(f"Time: {date_utils.convert_dt(self.date).strftime("%I:%M %p")}")
        print(f"Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

def game_title(game: MLBGame) -> str:
    
    return f"{game.name}"
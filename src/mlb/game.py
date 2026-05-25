from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
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
        print(f"Time: {convert_dt(self.date).strftime("%I:%M %p")}")
        print(f"Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

def convert_dt(s: str) -> datetime:
    utc_dt = datetime.fromisoformat(s.replace("Z", "+00:00"))

    return utc_dt.astimezone(ZoneInfo("America/Chicago"))

def game_title(game: MLBGame) -> str:
    
    return f"{game.name}"
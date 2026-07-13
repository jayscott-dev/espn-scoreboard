from dataclasses import dataclass
import utils.date as date_utils
from typing import Self
from base import Game

@dataclass
class FIFAGame(Game):
    name: str
    date: str
    description: str
    home_team: str
    away_team: str
    home_score: str
    away_score: str
    display_clock: str
    
    @classmethod
    def from_dict(cls, game: dict) -> Self:
       competitions = game.get("competitions", [])[0]
       
       home_team = ""
       home_score = ""
       away_team = ""
       away_score = ""

       teams = competitions.get("competitors", [])
       for team in teams:
            if team["homeAway"] == "home":
                home_team = team["team"]["name"]
                home_score = team["score"]
            else:
                away_team = team["team"]["name"]
                away_score = team["score"]
            
       return cls (
            name = game.get("name", ""),
            date = game.get("date", ""),
            description = game["status"]["type"]["description"],
            home_team = home_team,
            home_score = home_score,
            away_team = away_team,
            away_score = away_score,
            display_clock = game["status"]["displayClock"]
       ) 
    
    @property
    def title(self) -> str:
        return self.name
    
    @property
    def start_time(self) -> str:
        return date_utils.convert_dt(self.date).strftime("%I:%M %p")
    
    @property
    def start_date(self) -> str:
        return self.date
    
    @property
    def status_detail(self) -> str:
        return self.display_clock
    
    @property
    def status(self) -> str:
        return self.description

    def print_game_data(self):
        print(f"\n{game_title(self)}")
        print(f"Time: {self.start_time}")
        print(f"Score: {self.away_team} {self.away_score} - {self.home_team} {self.home_score} ({self.display_clock})")

def game_title(game: FIFAGame) -> str:
    return f"{game.name} ({game.description})"

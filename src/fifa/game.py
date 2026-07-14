from dataclasses import dataclass
import utils.date as date_utils
from typing import Self
from base import Game, Team
from fifa.team import FIFATeam

@dataclass
class FIFAGame(Game):
    name: str
    date: str
    teams: dict
    description: str
    display_clock: str
    
    @classmethod
    def from_dict(cls, game: dict) -> Self:
        competitions = game.get("competitions", [])[0]
       
        teams = {}
        for team in competitions.get("competitors", []):
            teams[team["homeAway"]] = FIFATeam.from_dict(team)
    
        return cls (
             name = game.get("name", ""),
             date = game.get("date", ""),
             teams = teams,
             description = game["status"]["type"]["description"],
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

    @property
    def home_team(self) -> Team:
        return self.teams["home"]
    
    @property
    def away_team(self) -> Team:
        return self.teams["away"]
    
    def print_game_data(self):
        print(f"\n{game_title(self)}")
        print(f"Time: {self.start_time}")
        print(f"Score: {self.away_team.name} {self.away_team.score} - {self.home_team.name} {self.home_team.score} ({self.display_clock})")

def game_title(game: FIFAGame) -> str:
    return f"{game.name} ({game.description})"

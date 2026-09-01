from __future__ import annotations
from base import Game, Team
from dataclasses import dataclass
from nfl.team import NFLTeam

import utils.date as date_utils

@dataclass
class NFLGame(Game):
    name: str
    date: str
    teams: dict

    @classmethod
    def from_dict(cls, game: dict) -> NFLGame:
        competitions = game.get("competitions", [])[0]

        teams = {}
        for team in competitions.get("competitors", []):
            teams[team["homeAway"]] = NFLTeam.from_dict(team)

        return cls(
            name = game.get("name", ""),
            teams = teams,
            date = game.get("date", ""),
        )

    @property
    def title(self) -> str:
        return self.name

    @property
    def start_date(self) -> str:
        return self.date
    
    @property
    def start_time(self) -> str:
        return date_utils.convert_dt(self.date).strftime("%I:%M %p")
    
    @property
    def status(self) -> str:
        # return self.metadata.status
        return "N/A"
    
    @property
    def status_detail(self) -> str:
        # return self.metadata.detail
        return "N/A"
    
    #@property
    #def series_info(self) -> str | None:
    #    if self.series_data:
    #      return f"{self.series_data} {self.build_series_record() if self.series_records else ""}"
        
    @property
    def home_team(self) -> Team:
        return self.teams["home"]
    
    @property
    def away_team(self) -> Team:
        return self.teams["away"]
    
    def print_game_data(self):
        print(f"\n{game_title(self)}")

def game_title(game: NFLGame) -> str:
    return f"{game.name}"
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
    metadata: GameMetadata

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
            metadata = GameMetadata.from_dict(competitions["status"]),
        )

    @property
    def title(self) -> str:
        return self.name

    @property
    def start_date(self) -> str:
        return self.date

    @property
    def formatted_date(self) -> str:
        return date_utils.format_dt(self.date, "%m/%d/%Y (%A)")
    
    @property
    def start_time(self) -> str:
        return date_utils.convert_dt(self.date).strftime("%I:%M %p")
    
    @property
    def status(self) -> str:
        return self.metadata.status
    
    @property
    def status_detail(self) -> str:
        return self.metadata.detail
    
    @property
    def home_team(self) -> Team:
        return self.teams["home"]
    
    @property
    def away_team(self) -> Team:
        return self.teams["away"]
    
    def print_game_data(self):
        print(f"\n{game_title(self)}")
        print(f"{self.formatted_date} - {self.start_time}")
        print(f"{'Final' if self.metadata.status == "Final" else 'Current'} Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

@dataclass
class GameMetadata:
    status: str
    detail: str

    @classmethod
    def from_dict(cls, metdata: dict) -> GameMetadata:
        status_type = metdata["type"]

        return cls (
            status = status_type["description"],
            detail = status_type["detail"],
        )

def game_title(game: NFLGame) -> str:
    game_status = game.metadata.detail if game.metadata.status == "In Progress" else game.metadata.status

    return f"{game.name} ({game_status})"
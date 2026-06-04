from dataclasses import dataclass
import utils.date as date_utils
from typing import Optional, Self
from mlb.team import MLBTeam

@dataclass
class MLBGame:
    name: str
    date: str
    teams: dict[str, MLBTeam]
    game_metadata: GameMetadata
    
    @classmethod
    def from_dict(cls, game: dict) -> Self:
       competitions = game.get("competitions", [])[0]
       
       teams = {}
       for team in competitions.get("competitors", []):
           teams[team["homeAway"]] = MLBTeam.from_dict(team)

       return cls (
           name = game.get("name", ""),
           date = game.get("date", ""),
           teams = teams,
           game_metadata = GameMetadata.from_dict(competitions)
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
    game_status = game.game_metadata.status
    if game.game_metadata.detail:
        game_status += f", {game.game_metadata.detail}"
    return f"{game.name} ({game_status})"

@dataclass
class GameMetadata:
    status: str
    detail: str

    @classmethod
    def from_dict(cls, game: dict) -> Self:
        
        return cls (
            status = game["status"]["type"]["detail"],
            detail = game.get("outsText", ""),
        )
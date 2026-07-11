from dataclasses import dataclass
import utils.date as date_utils
from typing import Optional, Self
from mlb.team import MLBTeam
from mlb.stat_leader import StatLeader
from base import Game

@dataclass
class MLBGame(Game):
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
    
    @property
    def title(self) -> str:
        return self.name

    def home_team(self) -> MLBTeam:
        return self.teams["home"]
    
    def away_team(self) -> MLBTeam:
        return self.teams["away"]

    def print_game_data(self):
        print(f"\n{game_title(self)}")
        print(f"Time: {date_utils.convert_dt(self.date).strftime("%I:%M %p")}")
        print(f"Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

        stat_leaders = []
        if (rbi_leader := self.find_rbi_leader()) is not None:
            stat_leaders.append(rbi_leader)

        if (batting_average_leader := self.find_batting_avg_leader()) is not None:
            stat_leaders.append(batting_average_leader)

        if (hr_leader := self.find_hr_leader()) is not None:
            stat_leaders.append(hr_leader)
        
        if stat_leaders:
            print("Leaders:")
        
        for stat_leader in stat_leaders:
            print(f"  {stat_leader.display_name}: {stat_leader.athlete_name}, {stat_leader.formatted_display()}")

    def find_batting_avg_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.batting_avg_leader())
        return StatLeader.overall_stat_leader(leaders)
    
    def find_rbi_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.rbi_leader())
        return StatLeader.overall_stat_leader(leaders)
    
    def find_hr_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.hr_leader())
        return StatLeader.overall_stat_leader(leaders)

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
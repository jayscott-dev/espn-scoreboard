from dataclasses import dataclass
import utils.date as date_utils
from typing import Optional
from nba.team import NBATeam
from nba.stat_leader import StatLeader

@dataclass
class NBAGame:
    name: str
    date: str
    teams: dict
    completed: bool
    series_data: str
    metadata: GameMetadata
    series_records: dict[str, SeriesRecord]

    @classmethod
    def from_dict(cls, game: dict) -> "NBAGame":
        competitions = game.get("competitions", [])[0]
        completed = competitions.get("status", {}).get("type", {}).get("completed", False)

        teams = {}
        for team in competitions.get("competitors", []):
            teams[team["homeAway"]] = NBATeam.from_dict(team)

        notes = competitions.get("notes", [])
        if notes:
            series_data = notes[0]["headline"]
        else:
            series_data = ""

        series_records = {}
        team_records = competitions.get("series", {}).get("competitors", [])
        for team_record in team_records:
            series_records[team_record["id"]] = SeriesRecord.from_dict(team_record)

        return cls(
            name = game.get("name", ""),
            date = game.get("date", ""),
            teams = teams,
            completed = completed,
            series_data = series_data, 
            metadata = GameMetadata.from_dict(competitions["status"]),
            series_records = series_records
        )

    def home_team(self) -> NBATeam:
        return self.teams["home"]
    
    def away_team(self) -> NBATeam:
        return self.teams["away"]
    
    def build_series_record(self) -> str:
        return f"({self.series_records[self.away_team().id].wins} - {self.series_records[self.home_team().id].wins})"

    def print_game_data(self):
        print(f"\n{game_title(self)}")
        if self.series_data:
          print(f"{self.series_data} {self.build_series_record() if self.series_records else ""}")
        print(f"Time: {date_utils.convert_dt(self.date).strftime("%I:%M %p")}")
        print(f"{'Final' if self.metadata.status == "Final" else 'Current'} Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

        stat_leaders = []
        if (points_leader := self.find_overall_points_leader()) is not None:
            stat_leaders.append(points_leader)
            
        if (rebounds_leader := self.find_overall_rebounds_leader()) is not None:
            stat_leaders.append(rebounds_leader)
        
        if (assists_leader := self.find_overall_assists_leader()) is not None:
            stat_leaders.append(assists_leader)
        
        if stat_leaders:
            print("Leaders:")
        
        for stat_leader in stat_leaders:
            print(f"  {stat_leader.display_name}: {stat_leader.athlete_name}, {stat_leader.value}")

    def find_overall_points_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.points_leader())
        return StatLeader.overall_stat_leader(leaders)

    def find_overall_rebounds_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.rebounds_leader())
        return StatLeader.overall_stat_leader(leaders)

    def find_overall_assists_leader(self) -> Optional[StatLeader]:
        leaders = []
        for team in self.teams.values():
            leaders.append(team.assists_leader())
        return StatLeader.overall_stat_leader(leaders)
    
@dataclass
class GameMetadata:
    status: str
    detail: str

    @classmethod
    def from_dict(cls, metadata: dict) -> "GameMetadata":
        status_type = metadata["type"]
        
        return cls (
            status = status_type["description"],
            detail = status_type["detail"],
        )
    
def game_title(game: NBAGame) -> str:
    game_status = game.metadata.detail if game.metadata.status == "In Progress" else game.metadata.status

    return f"{game.name} ({game_status})"

@dataclass
class SeriesRecord:
    id: str
    wins: int

    @classmethod
    def from_dict(cls, data: dict) -> "SeriesRecord":
        return cls (
            id = data["id"],
            wins = data["wins"],
        )

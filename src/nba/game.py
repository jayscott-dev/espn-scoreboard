from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from nba.team import NBATeam
from nba.stat_leader import StatLeader

@dataclass
class NBAGame:
    name: str
    date: str
    teams: dict
    completed: bool
    status: str
    series_data: str

    @classmethod
    def from_dict(cls, game: dict) -> "NBAGame":
        competitions = game.get("competitions", [])[0]
        completed = competitions.get("status", {}).get("type", {}).get("completed", False)

        # notes[0]["headline"]

        teams = {}
        for team in competitions.get("competitors", []):
            teams[team["homeAway"]] = NBATeam.from_dict(team)


        return cls(
            name = game.get("name", ""),
            date = game.get("date", ""),
            teams = teams,
            completed = completed,
            status = "Final" if completed else "Current",
            series_data = competitions.get("notes", [])[0]["headline"],
        )

    def home_team(self) -> NBATeam:
        return self.teams["home"]
    
    def away_team(self) -> NBATeam:
        return self.teams["away"]

    def print_game_data(self):
        print(f"\n{self.name}")
        print(f"{self.series_data}")
        print(f"Time: {convert_dt(self.date).strftime("%I:%M %p")}")
        print(f"{self.status} Score: {self.teams["away"].build_score_display()} - {self.teams["home"].build_score_display()}")

        points_leader = self.find_overall_points_leader()
        if points_leader is not None:
            print(f"Overall Points Leader: {points_leader.athlete_name}, {points_leader.value}")

        rebounds_leader = self.find_overall_rebounds_leader()
        if rebounds_leader is not None:
            print(f"Overall Rebounds Leader: {rebounds_leader.athlete_name}, {rebounds_leader.value}")
            
        assists_leader = self.find_overall_assists_leader()
        if assists_leader is not None:
            print(f"Overall Assists Leader: {assists_leader.athlete_name}, {assists_leader.value}")

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

def convert_dt(s: str) -> datetime:
    utc_dt = datetime.fromisoformat(s.replace("Z", "+00:00"))

    return utc_dt.astimezone(ZoneInfo("America/Chicago"))

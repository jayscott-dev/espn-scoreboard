from dataclasses import dataclass
from nba.stat_leader import StatLeader
from typing import Optional

@dataclass
class NBATeam:
    id: str
    name: str
    display_name: str
    home: bool
    score: str
    leaders: list

    @classmethod
    def from_dict(cls, competitor: dict) -> "NBATeam":
        team = competitor.get("team", {})
        return cls(
            id = team.get("id", ""),
            name = team.get("name", ""),
            display_name = team.get("displayName", ""),
            home = ("home" == competitor.get("home", "")),
            score = competitor.get("score", "0"),
            leaders = [StatLeader.from_dict(leader) for leader in competitor.get("leaders", [])],
        )
    
    def build_score_display(self) -> str:
        return f"{self.name} {self.score}"
    
    def points_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("points")

    def rebounds_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("rebounds")

    def assists_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("assists")

    def find_stat_leader(self, stat_type: str) -> Optional[StatLeader]:
        for leader in self.leaders:
            if leader.stat_type == stat_type:
                return leader
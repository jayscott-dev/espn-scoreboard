from dataclasses import dataclass
from typing import Optional, Self
from mlb.stat_leader import StatLeader
from base import Team

@dataclass
class MLBTeam(Team):
    _id: str
    _name: str
    _score: str
    leaders: list[StatLeader]

    @classmethod
    def from_dict(cls, competitor: dict) -> Self:
        team = competitor.get("team", {})
        return cls(
            _id = team.get("id", ""),
            _name = team.get("name", ""),
            _score = competitor.get("score", "0"),
            leaders = [leader for raw in competitor.get("leaders", []) if (leader := StatLeader.from_dict(raw)) is not None],
        )

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def score(self) -> str:
        return self._score
    
    def build_score_display(self) -> str:
        return f"{self.name} {self.score}"
    
    def rbi_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("RBIs")
    
    def batting_avg_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("avg")
    
    def hr_leader(self) -> Optional[StatLeader]:
        return self.find_stat_leader("homeRuns")
    
    def find_stat_leader(self, stat_type: str) -> Optional[StatLeader]:
        for leader in self.leaders:
            if leader.stat_type == stat_type:
                return leader
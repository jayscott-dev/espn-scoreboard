from dataclasses import dataclass
from typing import Optional

@dataclass
class MLBTeam:
    id: str
    name: str
    score: str

    @classmethod
    def from_dict(cls, competitor: dict) -> "MLBTeam":
        team = competitor.get("team", {})
        return cls(
            id = team.get("id", ""),
            name = team.get("name", ""),
            score = competitor.get("score", "0"),
        )

    def build_score_display(self) -> str:
        return f"{self.name} {self.score}"
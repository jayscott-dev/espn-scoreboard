from dataclasses import dataclass
from typing import Optional, Self
from base import Team

@dataclass
class FIFATeam(Team):
    _id: str
    _name: str
    _score: str

    @classmethod
    def from_dict(cls, competitor: dict) -> Self:
        team = competitor.get("team", {})
        return cls(
            _id = team.get("id", ""),
            _name = team.get("name", ""),
            _score = competitor.get("score", "0"),
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
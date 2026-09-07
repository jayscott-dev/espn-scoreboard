from __future__ import annotations
from base import Team
from dataclasses import dataclass
from nfl.stat_leader import StatLeader
from typing import Optional

@dataclass
class NFLTeam(Team):
    _id: str
    _name: str
    _score: str
    _record: TeamRecord

    @classmethod
    def from_dict(cls, competitor: dict) -> NFLTeam:
        team = competitor.get("team", {})
        return cls(
            _id = team.get("id", ""),
            _name = team.get("name", ""),
            _score = competitor.get("score", "0"),
            _record = TeamRecord.from_list(competitor.get("records", [])),
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
    
    @property
    def record(self) -> str:
        return self._record.overall 

    def build_score_display(self) -> str:
        return f"{self.name}({self.record}) {self.score}"

@dataclass
class TeamRecord:
    overall: str
    home: str
    away: str

    @classmethod
    def from_list(cls, records: list) -> TeamRecord:
        home_record = "" 
        away_record = ""
        overall_record = ""

        for record in records:
            match record["type"]:
                case "home":
                    home_record = record["summary"]
                case "away":
                    away_record = record["summary"]
                case _:
                    overall_record = record["summary"]
        return cls (
            home = home_record,
            away = away_record,
            overall = overall_record,
        )

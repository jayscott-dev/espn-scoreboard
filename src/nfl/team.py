from __future__ import annotations
from base import Team
from dataclasses import dataclass

@dataclass
class NFLTeam(Team):
    _id: str
    _name: str
    _score: str

    @classmethod
    def from_dict(cls, competitor: dict) -> NFLTeam:
        team = competitor.get("team", {})
        return cls(
            _id = team.get("id", ""),
            _name = team.get("name", ""),
            #display_name = team.get("displayName", ""),
            #home = ("home" == competitor.get("homeAway", "")),
            _score = competitor.get("score", "0"),
            #leaders = [leader for raw in competitor.get("leaders", []) if (leader := StatLeader.from_dict(raw)) is not None],
            #_record = TeamRecord.from_list(competitor.get("records", [])),
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
    
    #@property
    #def record(self) -> str:
    #    return self._record.overall 

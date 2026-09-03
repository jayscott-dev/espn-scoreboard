from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

import base

ALLOWED_STAT_TYPES = {
    "rushing",
    "rushingLeader",
    "passing",
    "passingLeader",
    "receiving",
    "receivingLeader",
}

@dataclass
class StatLeader(base.StatLeader):
    _team_id: str
    stat_type: str
    athlete_name: str
    value: int
    display_name: str
    display_value: str

    @classmethod
    def from_dict(cls, stat_leader: dict) -> Optional["StatLeader"]:
        stat_type = stat_leader["name"] 
        if stat_type not in ALLOWED_STAT_TYPES:
            return

        leaders = stat_leader["leaders"]
        display_name = stat_leader["displayName"]
        if leaders:
            return cls (
                _team_id = leaders[0]["team"]["id"],
                stat_type = stat_type,
                athlete_name = leaders[0]["athlete"]["displayName"],
                value = leaders[0]["value"],
                display_name = display_name.split(" ")[0],
                display_value = leaders[0]["displayValue"],
            )

    @property
    def team_id(self) -> str:
        return self._team_id

    @property
    def label(self) -> str:
        return self.display_name

    @property
    def name(self) -> str:
        return self.athlete_name

    @property
    def stat_value(self) -> str:
        return str(self.display_value) 

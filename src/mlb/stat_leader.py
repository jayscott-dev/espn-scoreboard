from dataclasses import dataclass
from typing import Optional, Self
import re

@dataclass
class StatLeader:
    stat_type: str # name
    display_name: str
    value: float
    display_value: str
    athlete_name: str # fullName

    @classmethod
    def from_dict(cls, stat_leader: dict) -> Optional[Self]:
        stat_type = stat_leader["name"]
        leaders = stat_leader["leaders"]
        display_name = stat_leader["displayName"]
        if leaders:
            return cls (
                stat_type = stat_type,
                display_name = display_name,
                value = leaders[0]["value"],
                display_value = leaders[0]["displayValue"],
                athlete_name = leaders[0]["athlete"]["fullName"],
            )
            
    @classmethod
    def overall_stat_leader(cls, leaders: list[Self]) -> Optional[Self]:
        overall_leader = None
        for leader in leaders:
            if overall_leader is None:
                overall_leader = leader
            else:
                if leader.value > overall_leader.value:
                    overall_leader = leader
        return overall_leader

    def formatted_display(self) -> str:
        if self.stat_type == "avg":
            return f"{self.value:.3f} {self.parse_at_bats()}"
        return f"{self.value}"
    
    def parse_at_bats(self) -> str:
        parts = self.display_value.split(", ")
        if parts and re.search(r"-", parts[0]):
            return f"({parts[0]})"
        return ""
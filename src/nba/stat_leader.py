from dataclasses import dataclass
from typing import Optional

@dataclass
class StatLeader:
    stat_type: str
    athlete_name: str
    value: int
    display_name: str

    @classmethod
    def from_dict(cls, stat_leader: dict) -> Optional["StatLeader"]:
        stat_type = stat_leader["name"] 
        leaders = stat_leader["leaders"]
        display_name = stat_leader["displayName"]
        if leaders:
            return cls(
                stat_type = stat_type,
                athlete_name = leaders[0]["athlete"]["shortName"],
                value = leaders[0]["value"],
                display_name = display_name.split(" ")[0]
            )
        
    @classmethod
    def overall_stat_leader(cls, leaders: list[StatLeader]) -> Optional[StatLeader]:
        overall_leader = None
        for leader in leaders:
            if overall_leader is None:
                overall_leader = leader 
            else:
                if leader.value > overall_leader.value:
                    overall_leader = leader
        return overall_leader
            

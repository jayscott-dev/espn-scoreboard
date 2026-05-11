from dataclasses import dataclass
from typing import Optional

@dataclass
class StatLeader:
    stat_type: str
    athlete_name: Optional[str] = None
    value: Optional[int] = None

    @classmethod
    def from_dict(cls, stat_leader: dict) -> "StatLeader":
        stat_type = stat_leader["name"] 
        leaders = stat_leader["leaders"]
        if leaders:
            return cls(
                stat_type = stat_type,
                athlete_name = leaders[0]["athlete"]["shortName"],
                value = leaders[0]["value"]
            )
        else:
            return cls(
                stat_type = stat_type
            )
        
    @classmethod
    def overall_stat_leader(cls, leaders: list[StatLeader]) -> Optional[StatLeader]:
        overall_leader = None
        for leader in leaders:
            if overall_leader is None:
                overall_leader = leader 
            else:
                if leader.value is not None and overall_leader.value is not None and leader.value > overall_leader.value:
                    overall_leader = leader
        return overall_leader
            

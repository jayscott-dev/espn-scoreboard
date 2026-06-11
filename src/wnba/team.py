from dataclasses import dataclass
#from nba.stat_leader import StatLeader
from typing import Optional, Self

@dataclass
class WNBATeam:
    id: str
    name: str
    display_name: str
    home: bool
    score: str
    #leaders: list
    record: TeamRecord

    @classmethod
    def from_dict(cls, competitor: dict) -> Self:
        team = competitor.get("team", {})
        return cls(
            id = team.get("id", ""),
            name = team.get("name", ""),
            display_name = team.get("displayName", ""),
            home = ("home" == competitor.get("homeAway", "")),
            score = competitor.get("score", "0"),
            #leaders = [leader for raw in competitor.get("leaders", []) if (leader := StatLeader.from_dict(raw)) is not None],
            record = TeamRecord.from_list(competitor.get("records", [])),
        )
    
    def build_score_display(self) -> str:
        return f"{self.name}({self.record.overall}) {self.score}"
    
    #def points_leader(self) -> Optional[StatLeader]:
    #    return self.find_stat_leader("points")

    #def rebounds_leader(self) -> Optional[StatLeader]:
    #    return self.find_stat_leader("rebounds")

    #def assists_leader(self) -> Optional[StatLeader]:
    #    return self.find_stat_leader("assists")

    #def find_stat_leader(self, stat_type: str) -> Optional[StatLeader]:
    #    for leader in self.leaders:
    #        if leader.stat_type == stat_type:
    #            return leader
@dataclass
class TeamRecord:
    overall: str
    home: str
    away: str

    @classmethod
    def from_list(cls, records: list) -> Self:
        home_record = ""
        away_record = ""
        overall_record = ""

        for record in records:
            match record["type"]:
                case "home":
                    home_record = record["summary"]
                case "road":
                    away_record = record["summary"]
                case _:
                    overall_record = record["summary"]
        return cls (
            home = home_record,
            away = away_record,
            overall = overall_record,
        )
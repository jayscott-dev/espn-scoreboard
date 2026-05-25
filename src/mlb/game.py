from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

@dataclass
class MLBGame:
    name: str
    date: str
    
    @classmethod
    def from_dict(cls, game: dict) -> "MLBGame":

       return cls (
           name = game.get("name", ""),
           date = game.get("date", ""),
       ) 
    
    def print_game_data(self):
        print(f"\n{game_title(self)}")

def game_title(game: MLBGame) -> str:
    
    return f"{game.name}"
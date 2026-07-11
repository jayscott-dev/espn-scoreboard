from abc import ABC, abstractmethod
from collections.abc import Sequence

class Scoreboard(ABC):
    @property
    def date_display(self) -> str:
        ...
    
    @property
    def games(self) -> Sequence[Game]:
        ...

    @property
    def league(self) -> str:
        ...

class Game(ABC):
    @property
    def title(self) -> str:
        ...
from abc import ABC, abstractmethod

class Scoreboard(ABC):
    @property
    def date_display(self) -> str:
        ...

    @property
    def league(self) -> str:
        ...

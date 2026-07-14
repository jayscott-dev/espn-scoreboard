from abc import ABC, abstractmethod
from collections.abc import Sequence

class Scoreboard(ABC):
    @property
    @abstractmethod
    def date_display(self) -> str:
        ...
    
    @property
    @abstractmethod
    def games(self) -> Sequence[Game]:
        ...

    @property
    @abstractmethod
    def league(self) -> str:
        ...

class Game(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        ...
    
    @property
    @abstractmethod
    def start_date(self) -> str:
        ...

    @property
    @abstractmethod
    def start_time(self) -> str:
        ...
    
    @property
    @abstractmethod
    def status(self) -> str:
        ...

    @property
    @abstractmethod
    def status_detail(self) -> str:
        ...
    @property
    def series_info(self) -> str | None:
        return None
    
    @property
    @abstractmethod
    def home_team(self) -> Team:
        ...

    @property
    @abstractmethod
    def away_team(self) -> Team:
        ...

class Team(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
    
    @property
    @abstractmethod
    def score(self) -> str:
        ...
    
    @property
    def record(self) -> str | None:
        return None
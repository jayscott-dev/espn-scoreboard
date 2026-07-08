from typing import Protocol, runtime_checkable

@runtime_checkable
class Scoreboard(Protocol):
    @property
    def date_display(self) -> str:
        ...

    @property
    def league(self) -> str:
        ...

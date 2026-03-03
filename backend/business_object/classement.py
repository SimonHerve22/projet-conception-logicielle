from dataclasses import dataclass


@dataclass
class RegularSeasonStanding:
    tournoi: str
    rang: int
    equipe: str
    score: str
    winrate: float
    streak: str


@dataclass
class PlayoffResult:
    tournoi: str
    place: str
    qualification: str
    equipe: str

from dataclasses import dataclass


@dataclass
class Match:
    tournoi: str
    date: str
    patch: str
    blue_team: str
    red_team: str
    winner: str

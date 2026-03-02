from dataclasses import dataclass


@dataclass
class PlayerStat:
    tournoi: str
    equipe: str
    name: str
    games: int
    wins: int
    losses: int
    winrate: float
    kda: float
    kill_participation: float
    main_champion: str

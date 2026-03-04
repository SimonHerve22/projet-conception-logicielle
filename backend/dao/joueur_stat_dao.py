from business_object.joueur_stat import (
    PlayerStat,
)  # Assure-toi que PlayerStat est dans ce module
from dao.db_connection import DBConnection


class PlayerStatDAO:
    def ajouter(self, player_stat: PlayerStat) -> None:
        """
        Ajoute un PlayerStat en base.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO player_stats (
                    tournoi, equipe, name, games, wins, losses, winrate, kda, kill_participation, main_champion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    player_stat.tournoi,
                    player_stat.equipe,
                    player_stat.name,
                    player_stat.games,
                    player_stat.wins,
                    player_stat.losses,
                    player_stat.winrate,
                    player_stat.kda,
                    player_stat.kill_participation,
                    player_stat.main_champion,
                ),
            )
            connection.commit()

        finally:
            cursor.close()

    def trouver(self, name: str, tournoi: str) -> PlayerStat | None:
        """
        Retourne un PlayerStat par nom et tournoi, ou None si non trouvé.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT tournoi, equipe, name, games, wins, losses, winrate, kda, kill_participation, main_champion "
                "FROM player_stats WHERE name = ? AND tournoi = ?;",
                (name, tournoi),
            )

            row = cursor.fetchone()
            if row is None:
                return None

            return PlayerStat(*row)

        finally:
            cursor.close()

    def supprimer(self, name: str, tournoi: str) -> None:
        """
        Supprime un PlayerStat par nom et tournoi.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM player_stats WHERE name = ? AND tournoi = ?;",
                (name, tournoi),
            )
            connection.commit()

        finally:
            cursor.close()

    def lister(self) -> list[PlayerStat]:
        """
        Retourne tous les PlayerStats.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT tournoi, equipe, name, games, wins, losses, winrate, kda, kill_participation, main_champion "
                "FROM player_stats;"
            )
            rows = cursor.fetchall()
            return [PlayerStat(*row) for row in rows]

        finally:
            cursor.close()

    def lister_par_tournoi(self, tournoi: str) -> list[PlayerStat]:
        """Retourne les PlayerStats d'un tournoi spécifique."""
        connection = DBConnection().connection
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT tournoi, equipe, name, games, wins, losses, winrate, kda, kill_participation, main_champion "
                "FROM player_stats WHERE tournoi = ?;",
                (tournoi,),
            )
            rows = cursor.fetchall()
            return [PlayerStat(*row) for row in rows]
        finally:
            cursor.close()

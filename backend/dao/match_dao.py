from business_object.match import Match
from dao.db_connection import DBConnection


class MatchDAO:
    def ajouter(self, match: Match) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT OR REPLACE INTO matches (
                    tournoi, date, patch, blue_team, red_team, winner
                ) VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    match.tournoi,
                    match.date,
                    match.patch,
                    match.blue_team,
                    match.red_team,
                    match.winner,
                ),
            )
            connection.commit()

        finally:
            cursor.close()

    def lister(self) -> list[Match]:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT tournoi, date, patch, blue_team, red_team, winner
                FROM matches;
                """
            )

            rows = cursor.fetchall()
            return [Match(*row) for row in rows]

        finally:
            cursor.close()

    def supprimer_par_tournoi(self, tournoi: str) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM matches WHERE tournoi = ?;",
                (tournoi,),
            )
            connection.commit()

        finally:
            cursor.close()

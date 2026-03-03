from business_object.classement import RegularSeasonStanding
from dao.db_connection import DBConnection


class RegularSeasonStandingDAO:
    def ajouter(self, standing: RegularSeasonStanding) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO regular_season_standings (
                    tournoi, rang, equipe, score, winrate, streak
                ) VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    standing.tournoi,
                    standing.rang,
                    standing.equipe,
                    standing.score,
                    standing.winrate,
                    standing.streak,
                ),
            )
            connection.commit()

        finally:
            cursor.close()

    def trouver(self, tournoi: str, rang: int) -> RegularSeasonStanding | None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT tournoi, rang, equipe, score, winrate, streak
                FROM regular_season_standings
                WHERE tournoi = ? AND rang = ?;
                """,
                (tournoi, rang),
            )

            row = cursor.fetchone()
            if row is None:
                return None

            return RegularSeasonStanding(*row)

        finally:
            cursor.close()

    def supprimer(self, tournoi: str, rang: int) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM regular_season_standings
                WHERE tournoi = ? AND rang = ?;
                """,
                (tournoi, rang),
            )
            connection.commit()

        finally:
            cursor.close()

    def lister(self) -> list[RegularSeasonStanding]:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT tournoi, rang, equipe, score, winrate, streak
                FROM regular_season_standings;
                """
            )

            rows = cursor.fetchall()
            return [RegularSeasonStanding(*row) for row in rows]

        finally:
            cursor.close()

from business_object.classement import PlayoffResult
from dao.db_connection import DBConnection


class PlayoffResultDAO:
    def ajouter(self, result: PlayoffResult) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO playoff_results (
                    tournoi, place, qualification, equipe
                ) VALUES (?, ?, ?, ?);
                """,
                (
                    result.tournoi,
                    result.place,
                    result.qualification,
                    result.equipe,
                ),
            )
            connection.commit()

        finally:
            cursor.close()

    def trouver(self, tournoi: str, place: str) -> PlayoffResult | None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT tournoi, place, qualification, equipe
                FROM playoff_results
                WHERE tournoi = ? AND place = ?;
                """,
                (tournoi, place),
            )

            row = cursor.fetchone()
            if row is None:
                return None

            return PlayoffResult(*row)

        finally:
            cursor.close()

    def supprimer(self, tournoi: str, place: str) -> None:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM playoff_results
                WHERE tournoi = ? AND place = ?;
                """,
                (tournoi, place),
            )
            connection.commit()

        finally:
            cursor.close()

    def lister(self) -> list[PlayoffResult]:
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT tournoi, place, qualification, equipe
                FROM playoff_results;
                """
            )

            rows = cursor.fetchall()
            return [PlayoffResult(*row) for row in rows]

        finally:
            cursor.close()

    def lister_par_tournoi(self, tournoi: str) -> list[PlayoffResult]:
        """Retourne les résultats de playoffs d'un tournoi spécifique."""
        connection = DBConnection().connection
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT tournoi, place, qualification, equipe
                FROM playoff_results
                WHERE tournoi = ?;
                """,
                (tournoi,),
            )
            rows = cursor.fetchall()
            return [PlayoffResult(*row) for row in rows]
        finally:
            cursor.close()

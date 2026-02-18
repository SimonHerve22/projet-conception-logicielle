from business_object.favoris import Favoris
from dao.db_connection import DBConnection


class FavorisDAO:

    def ajouter(self, favorite: Favoris) -> None:
        """
        Ajoute un favori en utilisant le pseudo utilisateur.
        Lève une exception si le pseudo n'existe pas.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            # Vérifie que l'utilisateur existe
            cursor.execute(
                "SELECT id FROM utilisateurs WHERE pseudo = ?;",
                (favorite.pseudo,)
            )
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f"L'utilisateur '{favorite.pseudo}' n'existe pas")

            user_id = result[0]

            # Ajoute le favori
            cursor.execute(
                "INSERT INTO favoris (user_id, team_name) VALUES (?, ?);",
                (user_id, favorite.team_name)
            )
            connection.commit()

        finally:
            cursor.close()

    def supprimer(self, pseudo: str, team_name: str) -> None:
        """
        Supprime un favori à partir du pseudo et du nom de l'équipe.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM favoris
                WHERE user_id = (SELECT id FROM utilisateurs WHERE pseudo = ?)
                AND team_name = ?;
                """,
                (pseudo, team_name)
            )
            connection.commit()

        finally:
            cursor.close()

    def lister(self, pseudo: str) -> list[Favoris]:
        """
        Liste tous les favoris d'un utilisateur à partir de son pseudo.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT u.pseudo, f.team_name
                FROM favoris f
                JOIN utilisateurs u ON f.user_id = u.id
                WHERE u.pseudo = ?;
                """,
                (pseudo,)
            )

            rows = cursor.fetchall()

            return [Favoris(row[0], row[1]) for row in rows]

        finally:
            cursor.close()

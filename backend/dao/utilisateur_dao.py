from business_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection


class UtilisateurDAO:
    def ajouter(self, utilisateur: Utilisateur) -> None:
        """
        Ajoute un utilisateur en base.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO utilisateurs (pseudo, hash_mdp) VALUES (?, ?);",
                (utilisateur.pseudo, utilisateur.hash_mdp),
            )
            connection.commit()

        finally:
            cursor.close()

    def trouver(self, pseudo: str) -> Utilisateur | None:
        """
        Retourne un utilisateur si trouvé, sinon None.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT pseudo, hash_mdp FROM utilisateurs WHERE pseudo = ?;", (pseudo,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Utilisateur(row[0], row[1])
        finally:
            cursor.close()

    def supprimer(self, pseudo: str) -> None:
        """
        Supprime un utilisateur par son pseudo.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM utilisateurs WHERE pseudo = ?;", (pseudo,))
            connection.commit()

        finally:
            cursor.close()

    def lister(self) -> list[Utilisateur]:
        """
        Retourne tous les utilisateurs.
        """
        connection = DBConnection().connection
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT pseudo, hash_mdp FROM utilisateurs;")
            rows = cursor.fetchall()

            return [Utilisateur(row[0], row[1]) for row in rows]

        finally:
            cursor.close()

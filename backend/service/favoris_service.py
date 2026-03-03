from business_object.favoris import Favoris
from dao.favoris_dao import FavorisDAO


class FavorisService:
    def __init__(self):
        self.dao = FavorisDAO()

    def ajouter_favori(self, pseudo: str, team_name: str) -> None:
        """
        Ajoute un favori pour un utilisateur.
        Vérifie les types et valeurs avant de passer au DAO.
        """
        favoris = Favoris(pseudo, team_name)
        self.dao.ajouter(favoris)

    def supprimer_favori(self, pseudo: str, team_name: str) -> None:
        """
        Supprime un favori pour un utilisateur.
        """
        if not pseudo or not isinstance(pseudo, str):
            raise ValueError("Le pseudo doit être une chaîne non vide")
        if not team_name or not isinstance(team_name, str):
            raise ValueError("Le nom de l'équipe doit être une chaîne non vide")

        self.dao.supprimer(pseudo.strip(), team_name.strip())

    def lister_favoris(self, pseudo: str) -> list[Favoris]:
        """
        Retourne la liste des favoris d'un utilisateur.
        """
        if not pseudo or not isinstance(pseudo, str):
            raise ValueError("Le pseudo doit être une chaîne non vide")

        return self.dao.lister(pseudo.strip())

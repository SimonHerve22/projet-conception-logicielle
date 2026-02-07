from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateurDAO import UtilisateurDAO


class UtilisateurService:
    def __init__(self, dao: UtilisateurDAO):
        self.dao = dao

    def creer_utilisateur(self, pseudo: str) -> Utilisateur:
        if self.dao.trouver(pseudo) is not None:
            raise ValueError("Ce pseudo existe déjà")

        utilisateur = Utilisateur(pseudo)
        self.dao.ajouter(utilisateur)
        return utilisateur

    def recuperer_utilisateur(self, pseudo: str) -> Utilisateur | None:
        return self.dao.trouver(pseudo)

    def supprimer_utilisateur(self, pseudo: str) -> None:
        self.dao.supprimer(pseudo)

    def lister_utilisateurs(self) -> list[Utilisateur]:
        return self.dao.lister()

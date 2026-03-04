from datetime import datetime  # noqa: N999
import os

import pytz
import requests
from utils.singleton import Singleton


class Session(metaclass=Singleton):
    """
    Stocke les données liées à la session locale :
    - Un seul utilisateur est connecté par terminal
    """

    def __init__(self):
        """Initialisation de la session"""
        self.pseudo = None
        self.mdp = None
        self.debut_connexion = None
        self.host = os.environ.get("HOST_WEBSERVICE")

    def connexion(self, pseudo: int, mdp: str):
        """Connexion d’un utilisateur en session locale"""
        self.pseudo = pseudo
        self.mdp = mdp
        self.debut_connexion = datetime.now(pytz.timezone("Europe/Paris")).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        print(f"utilisateur {pseudo} connecté à {self.debut_connexion}")

    def deconnexion(self):
        """Déconnexion du utilisateur local"""
        print(f"utilisateur {self.pseudo} déconnecté")
        self.pseudo = None
        self.debut_connexion = None

    def get_utilisateur(self) -> dict | None:
        """Récupère les infos du utilisateur depuis l’API"""
        if self.pseudo is None:
            return None
        try:
            resp = requests.get(
                f"{self.host}/utilisateur/verifier_creation/{self.pseudo}/{self.mdp}")
            if resp.status_code != 200:
                return None
            return resp.json()
        except Exception:
            return None

    def afficher(self) -> str:
        """Affiche les infos de la session et de la table"""
        res = "Actuellement en session :\n" + "-" * 30 + "\n"

        utilisateur = self.get_utilisateur()
        if not utilisateur:
            return res + "Impossible de récupérer les infos du utilisateur.\n"

        res += f"utilisateur connecté : {self.pseudo}"
        if self.debut_connexion:
            res += f"Début connexion : {self.debut_connexion}\n"

        return res

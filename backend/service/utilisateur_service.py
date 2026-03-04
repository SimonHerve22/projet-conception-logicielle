import bcrypt
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


class UtilisateurService:
    """
    Service d'authentification simple.
    Gère uniquement l'inscription et la vérification du mot de passe.
    """

    def __init__(self):
        self.dao = UtilisateurDAO()

    def inscrire(self, pseudo: str, mot_de_passe: str) -> bool:
        """
        Crée un nouvel utilisateur.
        Retourne True si succès, False si pseudo déjà existant.
        """
        if self.dao.trouver(pseudo) is not None:
            return False  # pseudo déjà pris

        # Hash du mot de passe
        hash_mdp = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt())

        utilisateur = Utilisateur(pseudo, hash_mdp)
        self.dao.ajouter(utilisateur)
        return True  # utilisateur

    def verifier_connexion(self, pseudo: str, mot_de_passe: str) -> bool:
        """
        Vérifie si le mot de passe correspond à l'utilisateur.
        Retourne True si valide, sinon False.
        """
        utilisateur = self.dao.trouver(pseudo)
        if utilisateur is None:
            return False

        if bcrypt.checkpw(mot_de_passe.encode(), utilisateur.hash_mdp):
            return utilisateur

        else:
            return False

    def supprimer(self, pseudo: str, mot_de_passe: str) -> bool:
        """
        Supprime un compte si le mot de passe est correct.
        """
        if not self.verifier_connexion(pseudo, mot_de_passe):
            return False

        self.dao.supprimer(pseudo)
        return True

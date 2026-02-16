from business_object.utilisateur import Utilisateur


class UtilisateurDAO:
    def ajouter(self, utilisateur: Utilisateur) -> None:
        """
        Ajoute un utilisateur.
        (à implémenter plus tard)
        """
        raise NotImplementedError

    def trouver(self, pseudo: str) -> Utilisateur | None:
        """
        Retourne un utilisateur si trouvé, sinon None.
        (à implémenter plus tard)
        """
        raise NotImplementedError

    def supprimer(self, pseudo: str) -> None:
        """
        Supprime un utilisateur.
        (à implémenter plus tard)
        """
        raise NotImplementedError

    def lister(self) -> list[Utilisateur]:
        """
        Retourne tous les utilisateurs.
        (à implémenter plus tard)
        """
        raise NotImplementedError
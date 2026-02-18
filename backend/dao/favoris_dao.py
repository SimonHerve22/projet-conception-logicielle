from business_object.favoris import Favoris


class FavorisDAO:
    def ajouter(self, favorite: Favoris):
        raise NotImplementedError("Not implemented")

    def supprimer(self, user_id: str, team_id: str):
        raise NotImplementedError("Not implemented")

    def lister(self, user_id: str):
        raise NotImplementedError("Not implemented")
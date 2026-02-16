from business_object.favoris import Favoris


class FavorisDAO:
    def add(self, favorite: Favoris):
        raise NotImplementedError("Not implemented")

    def remove(self, user_id: str, team_id: str):
        raise NotImplementedError("Not implemented")

    def list(self, user_id: str):
        raise NotImplementedError("Not implemented")

    def exists(self, user_id: str, team_id: str) -> bool:
        raise NotImplementedError("Not implemented")
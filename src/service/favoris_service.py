from src.business_object.favoris import Favoris
from src.dao.favorisDAO import FavorisDAO


class FavoriteService:
    def __init__(self, dao: FavorisDAO, team_api):
        self.dao = dao
        self.team_api = team_api

    def add_favorite(self, user_id: str, team_id: str):
        # Vérifier que l'équipe existe (via API)
        if not self.team_api.team_exists(team_id):
            raise ValueError("Equipe inconnue")

        # Vérifier doublon
        if self.dao.exists(user_id, team_id):
            raise ValueError("Déjà en favoris")

        fav = Favoris(user_id=user_id, team_id=team_id)
        self.dao.add(fav)
        return fav

    def remove_favorite(self, user_id: str, team_id: str):
        if not self.dao.exists(user_id, team_id):
            raise ValueError("Favori inexistant")

        self.dao.remove(user_id, team_id)

    def list_favorites(self, user_id: str):
        return self.dao.list(user_id)

from src.business_object.favoris import Favoris
from src.dao.favorisDAO import FavorisDAO
from src.league_service.league_api import LeagueAPI


class FavoriteService:
    def __init__(self):
        self.dao = FavorisDAO()
        self.team_api = LeagueAPI()

    def add_favorite(self, user_id: str, team_id: str):
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

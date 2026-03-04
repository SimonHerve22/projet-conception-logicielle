from dao.match_dao import MatchDAO
from infrastructure.match_scraper import LeaguepediaMatchScraper


class MatchService:
    def __init__(self):
        self.scraper = LeaguepediaMatchScraper()
        self.dao = MatchDAO()

    def _construire_tournoi(self, annee: int, split: str) -> str:
        orga = "EU_LCS" if annee <= 2018 else "LEC"
        saison_str = "Season_3" if annee == 2013 else f"{annee}_Season"
        split_clean = split.replace(" ", "_")

        return f"{orga}/{saison_str}/{split_clean}"

    def import_matches(self, annee: int, split: str) -> int:
        tournoi_path = self._construire_tournoi(annee, split)
        print(f"Import des matchs pour : {tournoi_path}")

        matches = self.scraper.fetch(tournoi_path)
        print(f"{len(matches)} matchs récupérés.")

        for match in matches:
            self.dao.ajouter(match)

        print("Import terminé.")
        return len(matches)

    def obtenir_matchs_split(self, annee: int, split: str) -> list:
        """Récupère les stats d'un split précis en base."""
        tournoi_path = self._construire_tournoi(annee, split)
        return self.dao.lister_par_tournoi(tournoi_path)

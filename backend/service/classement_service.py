from business_object.classement import (
    PlayoffResult,
    RegularSeasonStanding,
)
from dao.classement_playoffs_dao import PlayoffResultDAO
from dao.classement_saison_dao import RegularSeasonStandingDAO
from infrastructure.classement_scraper import (
    LeaguepediaStandingsScraper,
)


class StandingsService:
    def __init__(self):
        self.scraper = LeaguepediaStandingsScraper()
        self.regular_dao = RegularSeasonStandingDAO()
        self.playoff_dao = PlayoffResultDAO()

    # --------------------------------------------------
    # 🔽 Construction du path Leaguepedia
    # --------------------------------------------------

    def _construire_tournoi(self, annee: int, split: str) -> str:
        orga = "EU_LCS" if annee <= 2018 else "LEC"
        saison_str = "Season_3" if annee == 2013 else f"{annee}_Season"
        split_clean = split.replace(" ", "_")

        return f"{orga}/{saison_str}/{split_clean}"

    # --------------------------------------------------
    # 🔽 Import principal
    # --------------------------------------------------

    def import_standings(self, annee: int, split: str) -> int:
        """
        Scrape et persiste les standings (Regular ou Playoffs).
        Retourne le nombre d'éléments importés.
        """
        tournoi_path = self._construire_tournoi(annee, split)
        print(f"Import des standings pour : {tournoi_path}")

        # 🔹 Scraping
        results = self.scraper.fetch(tournoi_path)
        print(f"{len(results)} entrées récupérées du scraper.")

        # 🔹 Persistance selon le type
        count = 0

        for result in results:
            if isinstance(result, RegularSeasonStanding):
                self.regular_dao.ajouter(result)

            elif isinstance(result, PlayoffResult):
                self.playoff_dao.ajouter(result)

            count += 1

        print("Import terminé.")
        return count

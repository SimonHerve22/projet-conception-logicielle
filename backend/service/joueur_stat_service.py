from dao.joueur_stat_dao import PlayerStatDAO
from infrastructure.joueur_stat_scraper import LeaguepediaPlayerScraper


class PlayerStatService:
    def __init__(self):
        self.scraper = LeaguepediaPlayerScraper()
        self.dao = PlayerStatDAO()

    def _construire_tournoi(self, annee: int, split: str) -> str:
        """
        Construit le chemin du tournoi pour Leaguepedia.
        """
        orga = "EU_LCS" if annee <= 2018 else "LEC"
        saison_str = "Season_3" if annee == 2013 else f"{annee}_Season"
        split_clean = split.replace(" ", "_")
        return f"{orga}/{saison_str}/{split_clean}"

    def import_stats(self, annee: int, split: str) -> int:
        """
        Récupère les stats via le scraper et les persiste en base.
        Retourne le nombre de joueurs ajoutés/mis à jour.
        """
        tournoi_path = self._construire_tournoi(annee, split)
        print(f"Import des stats pour : {tournoi_path}")

        # 🔹 Scraping
        stats = self.scraper.fetch_stats(tournoi_path)
        print(f"{len(stats)} joueurs récupérés du scraper.")

        # 🔹 Persistance
        for stat in stats:
            self.dao.ajouter(stat)  # INSERT OR REPLACE dans le DAO

        print("Import terminé.")
        return len(stats)

    def obtenir_stats_split(self, annee: int, split: str) -> list:
        """
        Récupère les stats d'un split en base.
        Si absentes, lance le scraping automatiquement.
        """
        tournoi_path = self._construire_tournoi(annee, split)

        # 1. Tentative de récupération en base
        stats = self.dao.lister_par_tournoi(tournoi_path)

        # 2. Si rien en base, on déclenche l'import automatique
        if not stats:
            print(
                f"🔍 Stats non trouvées localement pour {tournoi_path}. Scraping en cours..."
            )
            self.import_stats(annee, split)
            # 3. On récupère les données fraîchement enregistrées
            stats = self.dao.lister_par_tournoi(tournoi_path)

        return stats

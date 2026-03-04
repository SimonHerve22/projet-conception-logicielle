# views/classement_view.py

# ------------- provisoire pour tester le code directement -------------
import os
import sys


# On ajoute le dossier parent (backend) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------- début du code non-provisoire -------------

from business_object.classement import PlayoffResult, RegularSeasonStanding
from service.classement_service import StandingsService


class ClassementView:
    def __init__(self):
        self.service = StandingsService()

    def afficher_menu(self):
        while True:
            print("\n" + "=" * 55)
            print("      📈 LEC STANDINGS & PLAYOFFS - DASHBOARD 📈")
            print("=" * 55)
            print("1. Importer un classement (Scraping -> DB)")
            print("2. Consulter un classement (Saison ou Playoffs)")
            print("3. Retour / Quitter")
            print("-" * 55)

            choix = input("Choisissez une option : ").strip()

            if choix == "1":
                self._menu_import()
            elif choix == "2":
                self._menu_liste()
            elif choix == "3":
                break
            else:
                print("⚠️ Option invalide.")

    def _menu_import(self):
        print("\n📥 IMPORTATION DEPUIS LEAGUEPEDIA")
        try:
            annee = int(input("Année (ex: 2026) : ").strip())
            split = input("Split (ex: Winter_Season, Winter_Playoffs) : ").strip()

            nb_imports = self.service.import_standings(annee, split)
            print(f"✅ Succès ! {nb_imports} entrées ont été enregistrées en base.")

        except ValueError:
            print("❌ Erreur : L'année doit être un nombre entier.")
        except Exception as e:
            print(f"❌ Erreur lors du scraping : {e}")

    def _menu_liste(self):
        print("\n--- CONSULTATION D'UN CLASSEMENT ---")
        try:
            annee = int(input("Année (ex: 2026) : ").strip())
            split = input("Split (ex: Winter_Season, Winter_Playoffs) : ").strip()

            # Le service gère le "Lazy Loading" et renvoie soit des RegularSeasonStanding soit des PlayoffResult
            results = self.service.obtenir_classement_split(annee, split)

        except ValueError:
            print("❌ Erreur : L'année doit être un nombre.")
            return
        except Exception as e:
            print(f"❌ Erreur lors de la récupération : {e}")
            return

        if not results:
            print("📭 Aucun classement trouvé (Base vide et rien sur le Wiki).")
            return

        # On détecte le type du premier élément pour savoir quel tableau afficher
        if isinstance(results[0], RegularSeasonStanding):
            self._afficher_tableau_regular(results)
        elif isinstance(results[0], PlayoffResult):
            self._afficher_tableau_playoffs(results)

    def _afficher_tableau_regular(self, standings: list[RegularSeasonStanding]):
        print("\n📊 CLASSEMENT - SAISON RÉGULIÈRE")
        # On trie par rang pour s'assurer que c'est dans l'ordre
        standings_tries = sorted(standings, key=lambda x: x.rang)

        header = f"{'Rang':<4} | {'Équipe':<25} | {'Score':<7} | {'Winrate':<7} | {'Streak':<6}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for s in standings_tries:
            print(
                f"#{s.rang:<3} | {s.equipe:<25} | {s.score:<7} | {s.winrate:<6.1f}% | {s.streak:<6}"
            )
        print("-" * len(header))

    def _afficher_tableau_playoffs(self, playoffs: list[PlayoffResult]):
        print("\n🏆 RÉSULTATS - PLAYOFFS")
        header = f"{'Place':<10} | {'Équipe':<25} | {'Qualification / Gains'}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for p in playoffs:
            # Nettoyage d'affichage si la place est vide (souvent le cas pour les éliminés très tôt)
            place_display = p.place if p.place else "-"
            print(f"{place_display:<10} | {p.equipe:<25} | {p.qualification}")
        print("-" * len(header))


# Point d'entrée pour tester la vue directement
if __name__ == "__main__":
    view = ClassementView()
    view.afficher_menu()

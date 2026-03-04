# view/joueur_stat_view.py

# ------------- provisoire pour tester le code directement -------------
import os
import sys


# On ajoute le dossier parent (backend) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------- début du code non-provisoire -------------

from service.joueur_stat_service import PlayerStatService


class PlayerStatView:
    def __init__(self):
        self.service = PlayerStatService()

    def afficher_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("      🏆 LEC PLAYER STATS - DASHBOARD 🏆")
            print("=" * 50)
            print("1. Importer des statistiques (Scraping -> DB)")
            print("2. Afficher toutes les statistiques en base")
            print("3. Quitter")
            print("-" * 50)

            choix = input("Choisissez une option : ").strip()

            if choix == "1":
                self._menu_import()
            elif choix == "2":
                self._menu_liste()
            elif choix == "3":
                print("À plus dans la Faille !")
                break
            else:
                print("Option invalide.")

    def _menu_import(self):
        print("\n--- IMPORTATION DEPUIS LEAGUEPEDIA ---")
        try:
            annee = int(input("Année (ex: 2025, 2026) : ").strip())
            split = input("Split (ex: Winter_Season, Versus_Season) : ").strip()

            nb_imports = self.service.import_stats(annee, split)
            print(f"Succès ! {nb_imports} joueurs ont été enregistrés en base.")

        except ValueError:
            print("Erreur : L'année doit être un nombre.")
        except Exception as e:
            print(f"Erreur lors de l'import : {e}")

    def _menu_liste(self):
        print("\n--- CONSULTATION DES STATISTIQUES ---")
        print("1. Afficher TOUTES les statistiques (historique global)")
        print("2. Consulter un SPLIT PRÉCIS (Scraping auto si besoin)")
        choix = input("Votre choix : ").strip()

        stats = []
        if choix == "1":
            stats = self.service.dao.lister()
        elif choix == "2":
            try:
                annee = int(input("Année (ex: 2025) : ").strip())
                split = input("Split (ex: Winter_Season) : ").strip()

                # Le service gère maintenant le "si vide -> scrape"
                stats = self.service.obtenir_stats_split(annee, split)

            except ValueError:
                print("❌ Erreur : L'année doit être un nombre.")
                return
            except Exception as e:
                print(f"❌ Erreur lors de la récupération : {e}")
                return
        else:
            print("⚠️ Choix invalide.")
            return

        if stats:
            self._afficher_tableau_stats(stats)
        else:
            print("📭 Aucune statistique trouvée (Base vide et rien sur le Wiki).")

    def _afficher_tableau_stats(self, stats):
        header = f"{'Split':<35} | {'Joueur':<15} | {'Équipe':<25} | {'Games':<5} | {'Winrate':<7} | {'KDA':<5} | {'KP % ':<6}"
        print("\n" + header)
        print("-" * len(header))

        for s in stats:
            print(
                f"{s.tournoi:<35} | {s.name:<15} | {s.equipe:<25} | {s.games:<5} | {s.winrate:<6.1f}% | {s.kda:<5.2f} | {s.kill_participation:<6.1f}%"
            )


# Point d'entrée pour tester la vue directement
if __name__ == "__main__":
    view = PlayerStatView()
    view.afficher_menu()

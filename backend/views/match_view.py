# views/match_view.py

# ------------- provisoire pour tester le code directement -------------
import os
import sys


# On ajoute le dossier parent (backend) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------- début du code non-provisoire -------------

from service.match_service import MatchService


class MatchView:
    def __init__(self):
        self.service = MatchService()

    def afficher_menu(self):
        while True:
            print("\n" + "═" * 60)
            print("      ⚔️  LEC MATCH HISTORY - DASHBOARD ⚔️")
            print("═" * 60)
            print("1. Importer l'historique d'un tournoi (Scraping -> DB)")
            print("2. Afficher tous les matchs enregistrés")
            print("3. Retour / Quitter")
            print("─" * 60)

            choix = input("Choisissez une option : ").strip()

            if choix == "1":
                self._menu_import()
            elif choix == "2":
                self._menu_liste()
            elif choix == "3":
                break
            else:
                print("⚠️  Choix inconnu, invoqueur.")

    def _menu_import(self):
        print("\n📥 IMPORTATION DEPUIS LEAGUEPEDIA")
        try:
            annee = int(input("Année (ex: 2026) : ").strip())
            split = input("Split (ex: Versus_Season) : ").strip()

            nb = self.service.import_matches(annee, split)
            print(f"✅ Terminé ! {nb} matchs ont été ajoutés ou mis à jour en base.")

        except ValueError:
            print("❌ Erreur : L'année doit être un nombre entier.")
        except Exception as e:
            print(f"❌ Erreur lors du scraping : {e}")

    def _menu_liste(self):
        print("\n--- CONSULTATION DE L'HISTORIQUE ---")
        print("1. Afficher TOUS les matchs en base")
        print("2. Consulter un SPLIT PRÉCIS (Scraping auto si besoin)")
        choix = input("Votre choix : ").strip()

        matches = []
        if choix == "1":
            matches = self.service.dao.lister()
        elif choix == "2":
            try:
                annee = int(input("Année (ex: 2026) : ").strip())
                split = input("Split (ex: Versus_Season) : ").strip()

                # Le service s'occupe de tout (check DB ou Scraping)
                matches = self.service.obtenir_matchs_split(annee, split)

            except ValueError:
                print("❌ Erreur : L'année doit être un nombre.")
                return
            except Exception as e:
                print(f"❌ Erreur lors de la récupération : {e}")
                return
        else:
            print("⚠️ Choix invalide.")
            return

        if matches:
            self._afficher_tableau_matchs(matches)
        else:
            print("Empty : Aucun match trouvé sur Leaguepedia pour ce split.")

    def _afficher_tableau_matchs(self, matches):
        """Affiche les matchs avec un formatage propre."""
        print("\n📜 RÉSULTATS DES MATCHS")
        # Formatage du header
        header = f"{'Split':<35} | {'Date':<12} | {'Patch':<7} | {'🔵 Blue Team':<20} | {'🔴 Red Team':<20} | {'🏆 Winner'}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for m in matches:
            # On ajoute une petite étoile visuelle pour le gagnant
            winner_display = f"⭐ {m.winner}"
            print(
                f"{m.tournoi:<35} | {m.date:<12} | {m.patch:<7} | {m.blue_team:<21} | {m.red_team:<21} | {winner_display}"
            )

        print("-" * len(header))
        print(f"Total : {len(matches)} matchs affichés.")


# Point d'entrée pour tester la vue directement
if __name__ == "__main__":
    view = MatchView()
    view.afficher_menu()

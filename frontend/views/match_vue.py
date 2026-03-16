import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class MatchVue(VueAbstraite):
    def afficher_menu(self):
        print("\n" + "═" * 60)
        print("      ⚔️  LEC MATCH HISTORY - DASHBOARD ⚔️")
        print("═" * 60)

        print("\n" + "-" * 50 + f"\n{self.jpseudo}\n" + "-" * 50 + "\n")
        print("Un exemple qui existe est LEC/2025_Season/Summer_Playoffs")

        annee = inquirer.text(message="Entrez l'année (ex:2025):").execute()
        annee = int(annee)

        splits_possibles = [
            "Spring_Season",
            "Spring_Playoffs",
            "Summer_Season",
            "Summer_Playoffs",
            "Winter_Season",
            "Winter_Groups",
            "Winter_Playoffs",
            "Spring_Groups",
            "Versus_Season",
            "Versus_Playoffs",
        ]

        split = inquirer.select(
            message="Choisissez le type de split :", choices=splits_possibles
        ).execute()

        # Construire l'URL pour l'API
        url = f"{host}/obtenir_stats/{annee}/{split}"

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            matchs = reponse.json()

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des matchs : {e}")

        self._afficher_tableau_matchs(matchs)

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=["Retour menu"],
        ).execute()

        if choix == "Retour menu":
            message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
            from views.menu_vue import MenuVue

            return MenuVue(message, temps_attente=1)

    def _afficher_tableau_matchs(self, matches: list[dict]):
        """Affiche les matchs avec un formatage propre."""
        print("\n📜 RÉSULTATS DES MATCHS")

        # Formatage du header
        header = f"{'Split':<35} | {'Date':<12} | {'Patch':<7} | {'🔵 Blue Team':<20} | {'🔴 Red Team':<20} | {'🏆 Winner'}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for m in matches:
            split = m.get("tournoi", "-")
            date = m.get("date", "-")
            patch = m.get("patch", "-")
            blue_team = m.get("blue_team", "-")
            red_team = m.get("red_team", "-")
            winner = m.get("winner", "-")

            winner_display = f"⭐ {winner}" if winner != "-" else "-"

            print(
                f"{split:<35} | {date:<12} | {patch:<7} | {blue_team:<21} | {red_team:<21} | {winner_display}"
            )

        print("-" * len(header))
        print(f"Total : {len(matches)} matchs affichés.")

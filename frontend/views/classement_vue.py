import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class ClassementVue(VueAbstraite):
    def choisir_menu(self):
        print("\n" + "=" * 50)
        print("      📈 Classement d'un split de LEC - Sélection 📈")
        print("=" * 50)

        print(f"\nUtilisateur : {Session().pseudo}\n")
        print("Veuillez renseigner les informations de votre split :")

        annee = inquirer.text(message="Entrez l'année (ex : 2025):").execute()
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
            message="Choisissez le type de split (Versus : uniquement 2026) :",
            choices=splits_possibles,
        ).execute()

        print("Obtention des données...")

        # Construire l'URL pour l'API
        url = f"{host}/obtenir_standings/{annee}/{split}"

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            standings = reponse.json()

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération du classement : {e}")

        print("\n--- CONSULTATION D'UN CLASSEMENT ---")

        # On détecte le type du premier élément pour savoir quel tableau afficher
        if "Playoffs" in split:
            self._afficher_tableau_playoffs(standings)
        else:
            self._afficher_tableau_regular(standings)

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=["Retour menu"],
        ).execute()

        if choix == "Retour menu":
            message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
            from views.menu_vue import MenuVue

            return MenuVue(message, temps_attente=1)

    def _afficher_tableau_regular(self, standings: list[dict]):
        print("\n📊 CLASSEMENT - SAISON RÉGULIÈRE")
        # On trie par rang pour s'assurer que c'est dans l'ordre
        standings_tries = sorted(standings, key=lambda x: x.get("rang", 0))

        header = f"{'Rang':<4} | {'Équipe':<25} | {'Score':<7} | {'Winrate':<7} | {'Streak':<6}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for s in standings_tries:
            rang = s.get("rang", "-")
            equipe = s.get("equipe", "-")
            score = s.get("score", "-")
            winrate = s.get("winrate", 0.0)
            streak = s.get("streak", "-")
            print(
                f"#{rang:<3} | {equipe:<25} | {score:<7} | {winrate:<6.1f}% | {streak:<6}"
            )
        print("-" * len(header))

    def _afficher_tableau_playoffs(self, playoffs: list[dict]):
        print("\n🏆 RÉSULTATS - PLAYOFFS")
        header = f"{'Place':<10} | {'Équipe':<25} | {'Qualification / Gains'}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for p in playoffs:
            # Utilisation de get() avec fallback si clé manquante ou None
            place_display = p.get("place") or "-"
            equipe = p.get("equipe", "-")
            qualification = p.get("qualification", "-")
            print(f"{place_display:<10} | {equipe:<25} | {qualification}")
        print("-" * len(header))

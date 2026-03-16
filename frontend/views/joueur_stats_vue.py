import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class JoueurStatsVue(VueAbstraite):
    """Vue d'un joueur"""

    def choisir_menu(self):
        """Boucle principale du menu recherche joueur pour l'ajout d'un favori."""
        print("\n" + "-" * 50 + f"\n{Session().pseudo}\n" + "-" * 50 + "\n")
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

        print("infos joueur")

        # Construire l'URL pour l'API
        url = f"{host}/obtenir_stats/{annee}/{split}"

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            stats = reponse.json()

            # Liste des pseudos
            pseudos = [joueur.get("name") for joueur in stats]

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des stats : {e}")

        actions = ["Retour menu"]

        actions += pseudos

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=actions,
        ).execute()

        if choix == "Retour menu":
            message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
            from views.menu_vue import MenuVue

            return MenuVue(message, temps_attente=1)

        if choix in pseudos:
            joueur = None
            for j in stats:
                if j.get("name") == choix:
                    joueur = j
                    break

            print(f"Équipe : {joueur.get('equipe')}")
            print(f"Tournoi : {joueur.get('tournoi', '')}")
            print(f"KDA : {joueur.get('kda')}")
            print(f"Winrate : {joueur.get('winrate')}%")

            choix = inquirer.select(
                message="Faites votre choix :",
                choices=["Retour menu"],
            ).execute()

            if choix == "Retour menu":
                message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
                from views.menu_vue import MenuVue

                return MenuVue(message, temps_attente=1)

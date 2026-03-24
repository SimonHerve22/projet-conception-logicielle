import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class InfoJoueurVue(VueAbstraite):
    """Vue d'un joueur"""

    def __init__(self, jpseudo: str, message="", temps_attente=0, input_attente=False):
        self.jpseudo = jpseudo
        super().__init__(message, temps_attente, input_attente)

    def choisir_menu(self):
        """Boucle principale du menu info joueur."""
        print(
            "\n"
            + "=" * 50
            + f"\nJoueur sélectionné : {self.jpseudo}\n"
            + "=" * 50
            + "\n"
        )
        print(
            "Veuillez renseigner les informations de votre split pour lesquelles vous souhaitez obtenir les informations du joueur :"
        )

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
            message="Choisissez le type de split :", choices=splits_possibles
        ).execute()

        print("Obtention des données...")

        # Construire l'URL pour l'API
        url = f"{host}/obtenir_stats/{annee}/{split}"

        try:
            reponse = requests.get(url)
            reponse.raise_for_status()
            stats = reponse.json()

            # Filtrer pour le joueur sélectionné
            joueur = None
            for j in stats:
                if j.get("name") == self.jpseudo:
                    joueur = j
                    break

            if joueur:
                print("Statistiques du joueur sur ce tournoi :")
                print(f"Tournoi : {joueur.get('tournoi', '')}")
                print(f"Équipe : {joueur.get('equipe')}")
                print(f"KDA : {joueur.get('kda')}")
                print(f"Winrate : {joueur.get('winrate')}%")
            else:
                print("Joueur non trouvé pour cette année/split.")

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des stats : {e}")

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=["Ajouter le joueur en favori", "Retour menu"],
        ).execute()

        if choix == "Ajouter le joueur en favori":
            url = f"{host}/favori/ajouter/{Session().pseudo}/{self.jpseudo}"
            try:
                requests.put(url)
            except ValueError:
                print("Erreur lors de l'ajout du favori")
            from views.favori_vue import FavoriVue

            return FavoriVue("")

        if choix == "Retour menu":
            from views.favori_vue import FavoriVue

            return FavoriVue("")

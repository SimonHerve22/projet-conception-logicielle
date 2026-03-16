import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class FavoriVue(VueAbstraite):
    """Vue de Favoris"""

    def choisir_menu(self):
        action_favoris = ["Retour au Menu", "Rechercher joueur favori"]

        print("\n" + "-" * 50 + "\nFavoris\n" + "-" * 50 + "\n")
        print("Retourner au menu recherche pour ajouter des joueurs favoris")

        # Récupération des favoris
        try:
            reponse = requests.get(f"{host}/favori/{Session().pseudo}")
            resultat = reponse.json()
            boutons_favoris = [favori["_Favoris__team_name"] for favori in resultat]
        except ValueError:
            boutons_favoris = []

        # Ajout des tables à l'interface
        action_favoris += boutons_favoris

        # Sélection du choix
        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_favoris,
        ).execute()

        # --- CAS FIXES ---
        if choix == "Retour au Menu":
            message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
            from views.menu_vue import MenuVue

            return MenuVue(message, temps_attente=1)

        if choix == "Rechercher joueur favori":
            message = f"Vous êtes connecté sous le pseudo {Session().pseudo}"
            from views.joueur_stats_vue import JoueurStatsVue

            return JoueurStatsVue(message, temps_attente=1)

        # --- CAS DES FAVORIS DYNAMIQUES ---
        if choix in boutons_favoris:
            from views.info_joueur_vue import InfoJoueurVue

            return InfoJoueurVue(choix)

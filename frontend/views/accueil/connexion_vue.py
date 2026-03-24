import os

from InquirerPy import inquirer
import requests
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/utilisateur"


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo)"""

    def choisir_menu(self):
        print("=" * 50 + "\n")
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mot_de_passe = inquirer.text(message="Entrez votre mot de passe : ").execute()

        url = f"{host}{END_POINT}/verifier_creation/{pseudo}/{mot_de_passe}"

        req = requests.get(url)
        if req.status_code != 200:
            message = req.json().get("detail", "Erreur inconnue")
            from views.accueil.accueil_vue import AccueilVue

            return AccueilVue(message, temps_attente=2)

        if not req.json():
            message = "le pseudo ou le mot de passe est incorrect"
            from views.accueil.accueil_vue import AccueilVue

            return AccueilVue(message, temps_attente=2)

        # Connexion dans la session (avec l'ID seulement)
        Session().connexion(pseudo, mot_de_passe)

        message = f"Vous êtes connecté sous le pseudo {pseudo}"
        from views.menu_vue import MenuVue

        return MenuVue(message, temps_attente=1)

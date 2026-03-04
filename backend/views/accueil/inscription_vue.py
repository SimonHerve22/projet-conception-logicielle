import os

from InquirerPy import inquirer
import requests
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/utilisateur"


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        valide = False
        while not valide:
            mot_de_passe = inquirer.text(
                message="Entrez votre mot de passe : "
            ).execute()
            mot_de_passe2 = inquirer.text(
                message="Veuillez confirmer votre mot de passe : "
            ).execute()
            if mot_de_passe == mot_de_passe2:
                valide = True

        # Appel de l'app pour créer l'utilisateur
        req = requests.post(f"{host}{END_POINT}/creation/{pseudo}/{mot_de_passe}")

        if req.status_code == 200:
            message = f"Votre compte {pseudo} a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = f"{req.status_code} {req.text} Erreur de connexion (pseudo ou mdp invalide)"

        from views.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)

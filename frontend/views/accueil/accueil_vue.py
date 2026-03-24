from InquirerPy import inquirer
from views.vue_abstraite import VueAbstraite


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print(
            "\n"
            + "=" * 50
            + "\nVeuillez vous connecter pour utiliser l'application.\n"
            + "Si vous n'avez pas encore de compte, créez-en un !\n"
            + "=" * 50
            + "\n"
        )

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Se connecter",
                "Créer un compte",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Se connecter":
                from views.accueil.connexion_vue import ConnexionVue

                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from views.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte joueur")

            case "Infos de session":
                from views.accueil.infos_session_vue import InfosSessionVue

                return InfosSessionVue("Chargement...", temps_attente=0)

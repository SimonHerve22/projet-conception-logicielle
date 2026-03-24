from InquirerPy import inquirer  # noqa: N999
from views.vue_abstraite import VueAbstraite


class MenuVue(VueAbstraite):
    """Vue du menu de l'application"""

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
            + "\nBienvenue sur l'application ! Que souhaitez-vous faire ?\n"
            + "=" * 50
            + "\n"
        )

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Recherche",
                "Gestion des favoris",
                "Infos de session",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from views.accueil.accueil_vue import AccueilVue

                return AccueilVue("Retour à l'accueil...")

            case "Gestion des favoris":
                from views.favori_vue import FavoriVue

                return FavoriVue("")

            case "Recherche":
                from views.recherche_vue import RechercheVue

                return RechercheVue("")

            case "Infos de session":
                from views.accueil.infos_session_vue import InfosSessionVue

                return InfosSessionVue("Chargement...", temps_attente=0)

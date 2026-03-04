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

        print("\n" + "-" * 50 + "\nMenu\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Recherche",
                "Gestion des favoris",
                "Retour",
                "Infos de session",
            ],
        ).execute()

        match choix:
            case "Retour":
                from views.accueil.accueil_vue import AccueilVue

                return AccueilVue("Accueil de l'application")

            case "Gestion des favoris":
                from views.favori_vue import FavoriVue

                return FavoriVue("Menu des favoris")

            case "Recherche":
                from views.recherche_view import RechercheVue

                return RechercheVue("Création de compte joueur")

            case "Infos de session":
                from views.accueil.InfosSessionVue import InfosSessionVue

                return InfosSessionVue("Chargement...", temps_attente=0)

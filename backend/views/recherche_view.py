# views/recherche_view.py

from InquirerPy import inquirer
from views.vue_abstraite import VueAbstraite


class RechercheVue(VueAbstraite):
    """Vue permettant de naviguer vers les différentes recherches de statistiques LEC"""

    def choisir_menu(self):
        """Choix du menu de statistiques

        Return
        ------
        view
            Retourne la vue elle-même après consultation, ou termine si "Retour"
        """
        print("\n" + "=" * 50)
        print("      🔎 RECHERCHE DE STATISTIQUES LEC 🔎")
        print("=" * 50 + "\n")

        choix = inquirer.select(
            message="Que souhaitez-vous consulter ? ",
            choices=[
                "Classements (Saison régulière & Playoffs)",
                "Historique des Matchs",
                "Statistiques des Joueurs",
                "Retour au menu précédent",
            ],
        ).execute()

        match choix:
            case "Classements (Saison régulière & Playoffs)":
                from views.classement_view import ClassementView

                # Lance la boucle de la vue des classements
                ClassementView().afficher_menu()

                # Une fois qu'on quitte (option 3), on relance cette même vue de recherche
                return RechercheVue("Retour au menu de recherche")

            case "Historique des Matchs":
                from views.match_view import MatchView

                MatchView().afficher_menu()
                return RechercheVue("Retour au menu de recherche")

            case "Statistiques des Joueurs":
                from views.joueur_stat_view import PlayerStatView

                PlayerStatView().afficher_menu()
                return RechercheVue("Retour au menu de recherche")

            case "Retour au menu précédent":
                from views.MenuVue import MenuVue

                return MenuVue("")

# views/recherche_view.py

from InquirerPy import inquirer
from views.vue_abstraite import VueAbstraite


class RechercheVue(VueAbstraite):
    """Vue permettant de naviguer vers les différentes recherches de statistiques LEC"""

    def choisir_menu(self):
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
                from views.classement_vue import ClassementVue

                return ClassementVue()

            case "Historique des Matchs":
                from views.match_vue import MatchVue

                return MatchVue()

            case "Statistiques des Joueurs":
                from views.joueur_stats_vue import JoueurStatsVue

                return JoueurStatsVue()

            case "Retour au menu précédent":
                from views.menu_vue import MenuVue

                return MenuVue("")

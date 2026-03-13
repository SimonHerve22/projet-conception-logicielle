import os

from views.accueil.accueil_vue import AccueilVue
from views.session import Session
from views.vue_abstraite import VueAbstraite


host = os.environ["HOST_WEBSERVICE"]


class InfosSessionVue(VueAbstraite):
    def choisir_menu(self):
        session = Session()
        res = "\n==================== INFOS SESSION ====================\n"

        # A) Joueur connecté dans CE terminal
        if session.pseudo is None:
            res += "Aucun joueur connecté dans ce terminal.\n"
            return AccueilVue(res, temps_attente=3)

        res += f"Joueur connecté : {session.pseudo}\n"
        res += (
            f"Début connexion : {getattr(session.pseudo, 'debut_connexion', 'N/A')}\n\n"
        )

        return MenuVue(res, temps_attente=3)

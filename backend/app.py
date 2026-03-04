from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from service.classement_service import StandingsService
from service.favoris_service import FavorisService
from service.joueur_stat_service import PlayerStatService
from service.match_service import MatchService
from service.utilisateur_service import UtilisateurService


app = FastAPI(title="LOL_API")

utilisateur_service = UtilisateurService()
favoris_service = FavorisService()
player_service = PlayerStatService()
standings_service = StandingsService()
match_service = MatchService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirection vers la documentation de l'API"""
    return RedirectResponse(url="/docs")


@app.get("/verifier_creation/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def verifier_creation(pseudo: str, mot_de_passe: str):
    """verifie l'existance d'un utilisateur"""
    return utilisateur_service.verifier_connexion(pseudo, mot_de_passe)


@app.post("/creation/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def creation(pseudo: str, mot_de_passe: str):
    """Creer un compte utilisateur"""
    return utilisateur_service.inscrire(pseudo, mot_de_passe)


@app.delete("/suppression_utilisateur/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def suppression_utilisateur(pseudo, mot_de_passe):
    """supprimme un compte utilisateur"""
    return utilisateur_service.supprimer(pseudo, mot_de_passe)


@app.put("/ajouter/{pseudo}/{team_name}", tags=["Favori"])
async def ajouterfavori(pseudo, team_name):
    """ajoute une equipe à la liste des favoris"""
    return favoris_service.ajouter_favori(pseudo, team_name)


@app.get("/{pseudo}", tags=["Favori"])
async def liste_favori(pseudo):
    """renvoie la liste des favoris"""
    return favoris_service.lister_favoris(pseudo)


@app.delete("/suppression/{pseudo}/{team_name}", tags=["Favori"])
async def suppression_favori(pseudo, team_name):
    """supprime une équipe des favoris"""
    return favoris_service.supprimer_favori(pseudo, team_name)


@app.get("/import_stats/{annee}/{split}", tags=["Statistiques"])
async def import_stats(annee, split):
    """Scrape et persiste les joueurs.
        Retourne le nombre d'éléments importés."""
    annee = int(annee)
    return player_service.import_stats(annee, split)


@app.get("/import_standings/{annee}/{split}", tags=["Statistiques"])
async def import_standings(annee, split):
    """Scrape et persiste les classements des équipes.
        Retourne le nombre d'éléments importés."""
    annee = int(annee)
    return standings_service.import_standings(annee, split)


@app.get("/import_matches/{annee}/{split}", tags=["Statistiques"])
async def import_matches(annee, split):
    """Scrape et persiste les matchs.
        Retourne le nombre d'éléments importés."""
    annee = int(annee)
    return match_service.import_matches(annee, split)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

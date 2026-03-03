from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from service.joueur_stat_service import PlayerStatService
from service.utilisateur_service import UtilisateurService


app = FastAPI(title="LOL_API")

utilisateur_service = UtilisateurService()
player_service = PlayerStatService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirection vers la documentation de l'API"""
    return RedirectResponse(url="/docs")


@app.get("/verifier_connexion/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def verifier_connexion(pseudo: str, mot_de_passe: str):
    """verifie la connection d'un utilisateur à son compte"""
    return utilisateur_service.verifier_connexion(pseudo, mot_de_passe)


@app.post("/creation/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def creation(pseudo: str, mot_de_passe: str):
    """Creer un compte utilisateur"""
    return utilisateur_service.inscrire(pseudo, mot_de_passe)


@app.delete("/suppression_utilisateur/{pseudo}/{mot_de_passe}", tags=["Utilisateur"])
async def suppression_utilisateur(pseudo, mot_de_passe):
    """supprimme un compte utilisateur"""
    return utilisateur_service.supprimer(pseudo, mot_de_passe)


@app.put("/modification", tags=["Utilisateur"])
async def modification():
    """modifie des informations de l'utilisateur"""
    return "votre compte a été modifié"


@app.put("/ajout", tags=["Favori"])
async def ajout_favori():
    """ajoute une equipe à la liste des favoris"""
    return "l'équipe à été ajouté"


@app.get("/", tags=["Favori"])
async def liste_favori():
    """renvoie la liste des favoris"""
    return "voici la liste des favoris"


@app.delete("/suppression", tags=["Favori"])
async def suppression_favori():
    """supprime une équipe des favoris"""
    return "l'equipe à été supprimé"


@app.get("/import_stats/{annee}/{split}", tags=["Statistiques"])
async def import_stats(annee, split):
    """affiche des stats"""
    annee = int(annee)
    return player_service.import_stats(annee, split)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

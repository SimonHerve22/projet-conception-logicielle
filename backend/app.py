from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(title="LOL_API")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirection vers la documentation de l'API"""
    return RedirectResponse(url="/docs")


@app.get("/connexion", tags=["Utilisateur"])
async def connexion():
    """Connecte un utilisateur à son compte"""
    return "vous etes connecté"


@app.post("/creation", tags=["Utilisateur"])
async def creation():
    """Creer un compte utilisateur"""
    return "votre compte est creé"


@app.delete("/suppression_utilisateur", tags=["Utilisateur"])
async def suppression_utilisateur():
    """supprimme un compte utilisateur"""
    return "votre compte est supprimmer"


@app.get("/visualisation_utilisateur", tags=["Utilisateur"])
async def visualisation_utilisateur():
    """Visualisation du compte de l'utilisateur"""
    return "voici les informations de votre compte"


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


@app.get("/stats", tags=["Statistiques"])
async def statistique():
    """affiche des stats"""
    return "voici les stats demandé"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

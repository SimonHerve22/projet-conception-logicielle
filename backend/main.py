from service.utilisateur_service import UtilisateurService
from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase


if __name__ == "__main__":
    initialiser_logs("Application")
    ResetDatabase().lancer()

    auth = UtilisateurService()

    # Inscription
    auth.inscrire("alice", "motDePasse123")

    # Connexion
    if auth.verifier_connexion("alice", "motDePasse123"):
        print("Connexion réussie")
    else:
        print("Échec connexion")

    auth.supprimer("alice", "motDePasse123")

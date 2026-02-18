from dao.utilisateur_dao import UtilisateurDAO
from dao.favoris_dao import FavorisDAO
from business_object.utilisateur import Utilisateur
from business_object.favoris import Favoris

def main():
    print("=== TEST DAO ===")

    # DAO
    utilisateur_dao = UtilisateurDAO()
    favoris_dao = FavorisDAO()

    # 1️⃣ Ajout d'utilisateurs
    print("\n--- Ajout d'utilisateurs ---")
    utilisateurs = [
        Utilisateur("alice"),
        Utilisateur("bob"),
        Utilisateur("charlie")
    ]

    for u in utilisateurs:
        try:
            utilisateur_dao.ajouter(u)
            print(f"Ajouté : {u}")
        except Exception as e:
            print(f"Erreur ajout {u}: {e}")

    # 2️⃣ Liste des utilisateurs
    print("\n--- Liste des utilisateurs ---")
    for u in utilisateur_dao.lister():
        print(u)

    # 3️⃣ Ajout de favoris
    print("\n--- Ajout de favoris ---")
    favoris = [
        Favoris("alice", "G2 Esports"),
        Favoris("alice", "Fnatic"),
        Favoris("bob", "Team Vitality"),
        Favoris("charlie", "MAD Lions KOI")
    ]

    for f in favoris:
        try:
            favoris_dao.ajouter(f)
            print(f"Favori ajouté : {f}")
        except Exception as e:
            print(f"Erreur ajout favori {f}: {e}")

    # 4️⃣ Liste des favoris par utilisateur
    print("\n--- Favoris par utilisateur ---")
    for u in ["alice", "bob", "charlie"]:
        user_favs = favoris_dao.lister(u)
        print(f"{u} : {user_favs}")

    # 5️⃣ Supprimer un favori
    print("\n--- Suppression d'un favori ---")
    favoris_dao.supprimer("alice", "Fnatic")
    print("Favori 'Fnatic' supprimé pour alice")
    print("Alice favoris : ", favoris_dao.lister("alice"))

    # 6️⃣ Supprimer un utilisateur
    print("\n--- Suppression d'un utilisateur ---")
    utilisateur_dao.supprimer("bob")
    print("Bob supprimé")
    print("Liste utilisateurs : ", utilisateur_dao.lister())
    print("Liste favoris Bob : ", favoris_dao.lister("bob"))

if __name__ == "__main__":
    main()

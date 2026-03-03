from business_object.joueur_stat import PlayerStat
from dao.joueur_stat_dao import PlayerStatDAO
from scrapper.scrapper import LeaguepediaPlayerScraper
from service.joueur_stat_service import PlayerStatService
from service.utilisateur_service import UtilisateurService
from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase


def test_player_stat_dao():
    dao = PlayerStatDAO()

    # 1️⃣ Créer un PlayerStat
    player = PlayerStat(
        tournoi="Spring Cup 2026",
        equipe="Team Phoenix",
        name="DragonSlayer",
        games=10,
        wins=7,
        losses=3,
        winrate=0.7,
        kda=3.5,
        kill_participation=0.65,
        main_champion="Ahri",
    )

    # 2️⃣ Ajouter le joueur à la base
    dao.ajouter(player)
    print("Ajout effectué.")

    # 3️⃣ Retrouver le joueur
    found = dao.trouver("DragonSlayer", "Spring Cup 2026")
    if found:
        print("Joueur trouvé :", found)
    else:
        print("Joueur non trouvé !")

    # 4️⃣ Lister tous les joueurs
    all_players = dao.lister()
    print(f"Total joueurs en base : {len(all_players)}")
    for p in all_players:
        print(p)

    # 5️⃣ Supprimer le joueur
    dao.supprimer("DragonSlayer", "Spring Cup 2026")
    print("Joueur supprimé.")

    # 6️⃣ Vérifier qu'il n'est plus là
    if dao.trouver("DragonSlayer", "Spring Cup 2026") is None:
        print("Suppression confirmée.")
    else:
        print("Erreur : le joueur est toujours présent !")


def test_scraper():
    scraper = LeaguepediaPlayerScraper()

    # 🔹 Remplace par un tournoi réel sur Leaguepedia
    tournoi = "LEC/2025_Season/Spring_Season"

    try:
        stats = scraper.fetch_stats(tournoi)
        print(f"{len(stats)} joueurs récupérés pour le tournoi {tournoi}.\n")

        for stat in stats[:5]:  # affiche juste les 5 premiers pour ne pas spammer
            print(stat)

    except Exception as e:
        print("Erreur lors du scraping :", e)


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

    test_player_stat_dao()
    test_scraper()

    service = PlayerStatService()
    nb_joueurs = service.import_stats(2025, "Spring_Season")
    print(f"{nb_joueurs} joueurs ajoutés/mis à jour en base.")

from bs4 import BeautifulSoup
import pandas as pd
import requests


# ------------------------------------------------------------
# FONCTIONS D'EXTRACTION (Inchangées)
# ------------------------------------------------------------


def extract_team_name(cell):
    link = cell.find("a")
    if link and link.get("title"):
        return link["title"]
    img = cell.find("img")
    if img and img.get("alt"):
        return img["alt"]
    return cell.get_text(strip=True)


def extract_first_champion(cell):
    link = cell.find("a", title=True)
    if link:
        return link["title"]
    img = cell.find("img", alt=True)
    if img:
        return img["alt"]
    span = cell.find(attrs={"data-champion": True})
    if span:
        return span["data-champion"]
    return ""


# ------------------------------------------------------------
# INTERACTION UTILISATEUR
# ------------------------------------------------------------

print("--- Générateur de statistiques joueurs Leaguepedia ---")

while True:
    try:
        # 1. Demande de l'année avec option de sortie
        entree = input("Année (ex: 2013, 2025) ou 'q' pour quitter : ").strip().lower()
        if entree == "q":
            print("Fermeture du programme. À bientôt !")
            break

        annee_input = int(entree)

        # 2. Demande du split
        split_input = input("Split (ex: Spring_Season, Winter_Playoffs) : ").strip()
        if split_input.lower() == "q":
            break

        split_clean = split_input.replace(" ", "_")

        # --- LOGIQUE DE CONSTRUCTION DU CHEMIN ---
        # Organisation
        # Organisation (Switch 2018/2019)
        orga = "EU_LCS" if annee_input <= 2018 else "LEC"

        # Nomenclature de la saison (Exception 2013)
        saison_str = "Season_3" if annee_input == 2013 else f"{annee_input}_Season"

        tournoi = f"{orga}/{saison_str}/{split_clean}"
        # -----------------------------------------

        print(f"Recherche : {tournoi}...")

        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": f"{tournoi}/Player_Statistics",
            "prop": "text",
            "format": "json",
        }

        res = requests.get(url, params=params)
        res_json = res.json()

        if "parse" not in res_json:
            print(f"Erreur : Page introuvable pour {tournoi}")
            print(
                f"Vérifiez ici : https://lol.fandom.com/wiki/{tournoi}/Player_Statistics\n"
            )
            continue

        html = res_json["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        table = soup.select_one("table.wikitable")
        if table is None:
            print(f"Pas de tableau trouvé sur la page {tournoi}.\n")
            continue

        rows = table.select("tr")
        data = []

        for row in rows[1:]:
            cols = row.select("th, td")
            cells = []
            for i, c in enumerate(cols):
                if i == 0:  # Team
                    cells.append(extract_team_name(c))
                elif i == len(cols) - 1:  # Champs
                    cells.append(extract_first_champion(c))
                else:
                    cells.append(c.get_text(strip=True))
            if cells:
                data.append(cells)

        df = pd.DataFrame(data)

        # Nettoyage header
        df = df.iloc[4:]

        if df.shape[1] == 23:
            df.columns = [
                "Equipe",
                "Name",
                "Games",
                "Wins",
                "Loses",
                "Winrate",
                "Kills/Game",
                "Deaths/Game",
                "Assists/Game",
                "KDA",
                "CS/Game",
                "CS/Min",
                "Vision/Game",
                "Vision/Min",
                "Golds/Game",
                "Golds/Min",
                "Damage/Game",
                "Damage/Min",
                "Kill Participation",
                "Kill Share",
                "Gold Share",
                "Nombre Champions",
                "Champs",
            ]
        else:
            print(f"Format inhabituel ({df.shape[1]} colonnes).")

        filename = f"exports_lec/{tournoi.replace('/', '_')}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"Succès ! Fichier enregistré : {filename}\n")
        print("-" * 40)

    except ValueError:
        print("Erreur : Veuillez entrer un nombre valide pour l'année.\n")
    except Exception as e:
        print(f"Erreur imprévue : {e}\n")

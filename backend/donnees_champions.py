import os
import time

from bs4 import BeautifulSoup
import pandas as pd
import requests


# ------------------------------------------------------------
# 🔧 FONCTIONS D'EXTRACTION ET PARSING
# ------------------------------------------------------------


def extract_champion_name(cell):
    """Extrait le nom du champion (image alt, lien title ou texte)."""
    img = cell.find("img", alt=True)
    if img:
        return img["alt"]
    link = cell.find("a", title=True)
    if link:
        return link["title"]
    return cell.get_text(strip=True)


def parse_champion_table(html, tournoi):
    """Parse le tableau HTML des statistiques de champions."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.wikitable")

    if table is None:
        print(f"Pas de tableau trouvé sur la page : {tournoi}")
        return None

    rows = table.select("tr")[1:]
    data = []

    for row in rows:
        cells = row.select("td")
        if not cells:
            continue

        row_data = []
        for i, cell in enumerate(cells):
            if i == 0:
                row_data.append(extract_champion_name(cell))
            else:
                row_data.append(cell.get_text(strip=True))
        data.append(row_data)

    if not data:
        return None

    df = pd.DataFrame(data)

    # Nettoyage des lignes d'en-tête complexes de Leaguepedia
    df = df.iloc[3:]

    # Définition des colonnes (basée sur ton format)
    # Note : Vérifie que le nombre de colonnes correspond bien à 25
    try:
        df.columns = [
            "Champion",
            "Games",
            "Pick/Ban%",
            "Bans",
            "Games_Play",
            "Nb Joueurs",
            "Wins",
            "Loses",
            "Winrate",
            "Kills/Game",
            "Morts/Game",
            "Assists/Game",
            "KDA",
            "Minions/Game",
            "Minions/Mins",
            "Vision/Game",
            "Vision/Mins",
            "Golds/Game",
            "Golds/Min",
            "Dégâts/Game",
            "Dégâts/Min",
            "Kill Participation",
            "Kill Share",
            "Gold Share",
            "Rôles",
        ]
    except ValueError as e:
        print(f"Alerte colonnes : {e}")
        print(f"Nombre de colonnes détectées : {df.shape[1]}")

    return df


# ------------------------------------------------------------
# 🚀 BOUCLE INTERACTIVE PRINCIPALE
# ------------------------------------------------------------

os.makedirs("exports_lec_champions", exist_ok=True)

print("=== Extracteur Leaguepedia CHAMPION Statistics ===")
print("(Tapez 'q' pour quitter)\n")

while True:
    try:
        # 1. Saisie de l'année
        entree_annee = input("Année (ex: 2013, 2018, 2025) ou 'q' : ").strip().lower()
        if entree_annee == "q":
            break

        annee_int = int(entree_annee)

        # 2. Saisie du split
        entree_split = input("Split (ex: Spring_Season, Summer_Playoffs) : ").strip()
        if entree_split.lower() == "q":
            break

        split_clean = entree_split.replace(" ", "_")

        # --- LOGIQUE DE CONSTRUCTION DU CHEMIN ---
        # Organisation (Switch 2018/2019)
        orga = "EU_LCS" if annee_int <= 2018 else "LEC"

        # Nomenclature de la saison (Exception 2013)
        saison_str = "Season_3" if annee_int == 2013 else f"{annee_int}_Season"

        tournoi_path = f"{orga}/{saison_str}/{split_clean}"
        # -----------------------------------------

        print(f"Scraping Champion Stats : {tournoi_path}...")

        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": f"{tournoi_path}/Champion_Statistics",
            "prop": "text",
            "format": "json",
        }

        res = requests.get(url, params=params)
        res_json = res.json()

        if "parse" not in res_json:
            print(f"Page absente : {tournoi_path}/Champion_Statistics")
            print(
                f"Vérifiez : https://lol.fandom.com/wiki/{tournoi_path}/Champion_Statistics\n"
            )
            continue

        html_content = res_json["parse"]["text"]["*"]
        df_result = parse_champion_table(html_content, tournoi_path)

        if df_result is not None and not df_result.empty:
            # 📁 Export CSV
            filename = f"exports_lec_champions/{tournoi_path.replace('/', '_')}.csv"
            df_result.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"Sauvegardé : {filename}\n")
        else:
            print("Aucune donnée n'a pu être extraite du tableau.\n")

        # Petite pause pour respecter le serveur
        time.sleep(0.5)
        print("-" * 40)

    except ValueError:
        print("Erreur : L'année doit être un nombre entier.\n")
    except Exception as e:
        print(f"Erreur imprévue : {e}\n")

print("Fermeture du programme. À bientôt !")

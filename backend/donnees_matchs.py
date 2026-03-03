import os

from bs4 import BeautifulSoup
import pandas as pd
import requests


# Création du dossier d'export s'il n'existe pas
if not os.path.exists("exports_matches"):
    os.makedirs("exports_matches")

# ------------------------------------------------------------
# FONCTIONS D'EXTRACTION
# ------------------------------------------------------------


def extract_cell_value(cell, is_team_column=False):
    """
    Extrait le texte ou le nom de l'équipe (via l'attribut title du lien ou alt de l'image).
    """
    if is_team_column:
        # Cherche d'abord un lien (souvent le title contient le nom propre de l'équipe)
        link = cell.find("a")
        if link and link.get("title"):
            return link["title"]
        # Sinon cherche l'image
        img = cell.find("img")
        if img and img.get("alt"):
            return img["alt"]

    # Par défaut, on prend le texte brut
    return cell.get_text(strip=True)


# ------------------------------------------------------------
# INTERACTION UTILISATEUR
# ------------------------------------------------------------

print("--- Extracteur d'historique de matchs Leaguepedia ---")

while True:
    try:
        entree = input("Année (ex: 2026) ou 'q' pour quitter : ").strip().lower()
        if entree == "q":
            break

        annee_input = int(entree)
        split_input = input("Split (ex: Versus_Season, Spring_Season) : ").strip()

        split_clean = split_input.replace(" ", "_")
        orga = "EU_LCS" if annee_input <= 2018 else "LEC"
        saison_str = "Season_3" if annee_input == 2013 else f"{annee_input}_Season"

        # Construction du tournoi et de la page Match_History
        tournoi = f"{orga}/{saison_str}/{split_clean}"
        print(f"Recherche de l'historique pour : {tournoi}...")

        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": f"{tournoi}/Match_History",
            "prop": "text",
            "format": "json",
        }

        res = requests.get(url, params=params)
        res_json = res.json()

        if "parse" not in res_json:
            print(f"Erreur : Page Match_History introuvable pour {tournoi}")
            continue

        html = res_json["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        # On cible le tableau avec la classe mhgame
        table = soup.select_one("table.mhgame")
        if table is None:
            print("Pas de tableau de matchs trouvé.\n")
            continue

        # Extraction des lignes du corps du tableau (tbody)
        rows = table.select("tbody tr")
        data = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            # On ne récupère que les 5 premières colonnes : Date, P, Blue, Red, Winner
            match_data = [
                extract_cell_value(cols[0]),  # Date
                extract_cell_value(cols[1]),  # P (Patch)
                extract_cell_value(cols[2], is_team_column=True),  # Blue
                extract_cell_value(cols[3], is_team_column=True),  # Red
                extract_cell_value(cols[4], is_team_column=True),  # Winner
            ]
            data.append(match_data)

        # Création du DataFrame
        df = pd.DataFrame(data, columns=["Date", "P", "Blue", "Red", "Winner"])

        # Sauvegarde
        filename = f"exports_matches/{tournoi.replace('/', '_')}_History.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"Succès ! {len(df)} matchs extraits dans : {filename}\n")
        print("-" * 40)

    except ValueError:
        print("Erreur : Entrez une année valide.\n")
    except Exception as e:
        print(f"Erreur : {e}\n")

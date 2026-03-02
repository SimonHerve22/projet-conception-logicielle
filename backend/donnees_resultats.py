import os

from bs4 import BeautifulSoup
import pandas as pd
import requests


# ------------------------------------------------------------
# FONCTIONS D'EXTRACTION DE DONNÉES
# ------------------------------------------------------------


def extract_team_name(cell):
    """Extrait le nom propre de l'équipe via la classe teamname."""
    team_span = cell.select_one(".teamname")
    if team_span:
        return team_span.get_text(strip=True)
    return cell.get_text(strip=True)


def parse_results_table(soup, is_playoff):
    """Détecte et parse le bon tableau selon le type de split."""
    data = []

    if is_playoff:
        # --- CAS PLAYOFFS (Tableau Place / Qualification / Team) ---
        # On cherche la table qui contient la classe spécifique aux résultats
        table = soup.find("td", class_="tournament-results-team")
        if not table:
            return None
        table = table.find_parent("table")

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 3:
                place = cols[0].get_text(strip=True)
                qualif = cols[1].get_text(strip=True)
                team = extract_team_name(cols[2])
                data.append([place, qualif, team])

        return pd.DataFrame(data, columns=["Place", "Qualification", "Equipe"])

    else:
        # --- CAS REGULAR SEASON (Tableau Rang / Team / Score / Winrate / Streak) ---
        table = soup.select_one("table.standings")
        if not table:
            return None

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            # Format Standings : Rang (0), Team (1), Win-Loss (2), % (3), Streak (4)
            if len(cols) >= 5:
                rank = cols[0].get_text(strip=True)
                team = extract_team_name(cols[1])
                score = cols[2].get_text(strip=True)
                winrate = cols[3].get_text(strip=True)
                streak = cols[4].get_text(strip=True)
                data.append([rank, team, score, winrate, streak])

        return pd.DataFrame(
            data, columns=["Rang", "Equipe", "Score", "Winrate", "Streak"]
        )


# ------------------------------------------------------------
# 🚀 BOUCLE PRINCIPALE INTERACTIVE
# ------------------------------------------------------------

os.makedirs("exports_lec_results", exist_ok=True)

print("=== Extracteur de Classements Leaguepedia (Standings/Results) ===")
print("(Tapez 'q' pour quitter)\n")

while True:
    try:
        # 1. Entrées utilisateur
        entree_annee = input("Année (ex: 2013, 2018, 2026) : ").strip().lower()
        if entree_annee == "q":
            break

        annee_int = int(entree_annee)
        split_input = input("Split (ex: Versus_Season, Spring_Playoffs) : ").strip()
        if split_input.lower() == "q":
            break

        split_clean = split_input.replace(" ", "_")

        # 2. Logique de construction d'URL (Identique à vos besoins)
        orga = "EU_LCS" if annee_int <= 2018 else "LEC"
        saison_str = "Season_3" if annee_int == 2013 else f"{annee_int}_Season"

        # NOTE : On ne rajoute pas /Player_Statistics ici !
        page_path = f"{orga}/{saison_str}/{split_clean}"
        is_playoff = "Playoffs" in split_clean

        print(f"Récupération de la page : {page_path}...")

        # 3. Requête API
        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": page_path,
            "prop": "text",
            "format": "json",
        }

        res = requests.get(url, params=params).json()

        if "parse" not in res:
            print(f"Erreur : Page '{page_path}' introuvable sur le wiki.\n")
            continue

        # 4. Parsing et Export
        html_content = res["parse"]["text"]["*"]
        soup = BeautifulSoup(html_content, "html.parser")

        df_result = parse_results_table(soup, is_playoff)

        if df_result is not None and not df_result.empty:
            filename = f"exports_lec_results/{page_path.replace('/', '_')}.csv"
            df_result.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"Classement exporté : {filename}\n")
        else:
            print("Impossible de trouver le tableau de classement sur cette page.\n")

        print("-" * 40)

    except ValueError:
        print("L'année doit être un nombre.\n")
    except Exception as e:
        print(f"Une erreur est survenue : {e}\n")

print("Programme terminé.")

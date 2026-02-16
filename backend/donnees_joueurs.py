from bs4 import BeautifulSoup
import pandas as pd
import os
import requests



liste_tournois = [
    "EU_LCS/Season_3/Spring_Season",
    "EU_LCS/Season_3/Spring_Playoffs",
    "EU_LCS/Season_3/Summer_Season",
    "EU_LCS/Season_3/Summer_Playoffs",
    "EU_LCS/2014_Season/Spring_Season",
    "EU_LCS/2014_Season/Spring_Playoffs",
    "EU_LCS/2014_Season/Summer_Season",
    "EU_LCS/2014_Season/Summer_Playoffs",
    "EU_LCS/2015_Season/Spring_Season",
    "EU_LCS/2015_Season/Spring_Playoffs",
    "EU_LCS/2015_Season/Summer_Season",
    "EU_LCS/2015_Season/Summer_Playoffs",
    "EU_LCS/2016_Season/Spring_Season",
    "EU_LCS/2016_Season/Spring_Playoffs",
    "EU_LCS/2016_Season/Summer_Season",
    "EU_LCS/2016_Season/Summer_Playoffs",
    "EU_LCS/2017_Season/Spring_Season",
    "EU_LCS/2017_Season/Spring_Playoffs",
    "EU_LCS/2017_Season/Summer_Season",
    "EU_LCS/2017_Season/Summer_Playoffs",
    "EU_LCS/2018_Season/Spring_Season",
    "EU_LCS/2018_Season/Spring_Playoffs",
    "EU_LCS/2018_Season/Summer_Season",
    "EU_LCS/2018_Season/Summer_Playoffs",
    "LEC/2019_Season/Spring_Season",
    "LEC/2019_Season/Spring_Playoffs",
    "LEC/2019_Season/Summer_Season",
    "LEC/2019_Season/Summer_Playoffs",
    "LEC/2020_Season/Spring_Season",
    "LEC/2020_Season/Spring_Playoffs",
    "LEC/2020_Season/Summer_Season",
    "LEC/2020_Season/Summer_Playoffs",
    "LEC/2021_Season/Spring_Season",
    "LEC/2021_Season/Spring_Playoffs",
    "LEC/2021_Season/Summer_Season",
    "LEC/2021_Season/Summer_Playoffs",
    "LEC/2022_Season/Spring_Season",
    "LEC/2022_Season/Spring_Playoffs",
    "LEC/2022_Season/Summer_Season",
    "LEC/2022_Season/Summer_Playoffs",
    "LEC/2023_Season/Winter_Season",
    "LEC/2023_Season/Winter_Groups",
    "LEC/2023_Season/Winter_Playoffs",
    "LEC/2023_Season/Spring_Season",
    "LEC/2023_Season/Spring_Groups",
    "LEC/2023_Season/Spring_Playoffs",
    "LEC/2023_Season/Summer_Season",
    "LEC/2023_Season/Summer_Groups",
    "LEC/2023_Season/Summer_Playoffs",
    "LEC/2024_Season/Winter_Season",
    "LEC/2024_Season/Winter_Playoffs",
    "LEC/2024_Season/Spring_Season",
    "LEC/2024_Season/Spring_Playoffs",
    "LEC/2024_Season/Summer_Season",
    "LEC/2024_Season/Summer_Playoffs",
    "LEC/2025_Season/Winter_Season",
    "LEC/2025_Season/Winter_Playoffs",
    "LEC/2025_Season/Spring_Season",
    "LEC/2025_Season/Spring_Playoffs",
    "LEC/2025_Season/Summer_Season",
    "LEC/2025_Season/Summer_Playoffs",
    "LEC/2026_Season/Versus_Season",
    "LEC/2026_Season/Versus_Playoffs",
]
os.makedirs("exports_lec", exist_ok=True)

all_data = {}

def extract_team_name(cell):
    # lien cliquable
    link = cell.find("a")
    if link and link.get("title"):
        return link["title"]

    # image alt
    img = cell.find("img")
    if img and img.get("alt"):
        return img["alt"]

    # fallback texte
    return cell.get_text(strip=True)

def extract_first_champion(cell):
    # lien direct
    link = cell.find("a", title=True)
    if link:
        return link["title"]

    # image avec alt
    img = cell.find("img", alt=True)
    if img:
        return img["alt"]

    # attribut data-champion
    span = cell.find(attrs={"data-champion": True})
    if span:
        return span["data-champion"]

    return ""

for tournoi in liste_tournois:
    try:
        print(f"Scraping : {tournoi}")

        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": f"{tournoi}/Player_Statistics",
            "prop": "text",
            "format": "json"
        }

        res = requests.get(url, params=params)
        res_json = res.json()

        if "parse" not in res_json:
            print(f"❌ Page absente : {tournoi}")
            continue

        html = res_json["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        table = soup.select_one("table.wikitable")
        if table is None:
            print(f"❌ Pas de table : {tournoi}")
            continue

        rows = table.select("tr")
        data = []

        for row in rows[1:]:
            cells = []
            cols = row.select("th, td")
            for i, c in enumerate(cols):
                if i == 0:  # Team
                    cells.append(extract_team_name(c))
                elif i == len(cols) - 1: # Champs
                    cells.append(extract_first_champion(c))
                else:
                    cells.append(c.get_text(strip=True))
            if cells:
                data.append(cells)

        df = pd.DataFrame(data)
        df = df.iloc[4:]

        # sécurité colonnes
        if df.shape[1] != 23:
            print(f"⚠ Colonnes inattendues ({df.shape[1]}) : {tournoi}")
            continue

        df.columns = [
            "Equipe","Name","Games","Wins","Loses","Winrate","Kills/Game","Deaths/Game",
            "Assists/Game","KDA","CS/Game","CS/Min","Vision/Game","Vision/Min",
            "Golds/Game","Golds/Min","Damage/Game","Damage/Min","Kill Participation",
            "Kill Share","Gold Share","Nombre Champions","Champs"
        ]

        filename = f"exports_lec/{tournoi.replace('/', '_')}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

    except Exception as e:
        print(f"Erreur pour {tournoi} : {e}")

print("✔ Terminé")
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time

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

os.makedirs("exports_lec_champions", exist_ok=True)

# 🔧 Fonction extraction nom champion depuis cellule image
def extract_champion_name(cell):
    img = cell.find("img", alt=True)
    if img:
        return img["alt"]

    link = cell.find("a", title=True)
    if link:
        return link["title"]

    return cell.get_text(strip=True)

# 🔧 Fonction parsing tableau
def parse_champion_table(html, tournoi):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.wikitable")

    if table is None:
        print(f"❌ Pas de table : {tournoi}")
        return None

    headers = [th.get_text(strip=True) for th in table.select("tr th")]
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

    df = pd.DataFrame(data)
    df = df.iloc[3:]

    df.columns = [
            "Champion", "Games", "Pick/Ban%", "Bans", "Games", "Nb Joueurs", "Wins", 
            "Loses", "Winrate", "Kills/Game", "Morts/Game", "Assists/Game", "KDA",
            "Minions/Game", "Minions/Mins", "Vision/Game", "Vision/Mins", "Golds/Game", 
            "Golds/Min", "Dégâts/Game", "Dégâts/Min", "Kill Participation", 
            "Kill Share", "Gold Share", "Rôles"
        ]

    return df

# 🚀 Scraping principal
for tournoi in liste_tournois:
    try:
        print(f"Scraping Champion Stats : {tournoi}")

        url = "https://lol.fandom.com/api.php"
        params = {
            "action": "parse",
            "page": f"{tournoi}/Champion_Statistics",
            "prop": "text",
            "format": "json"
        }

        res = requests.get(url, params=params)
        res_json = res.json()

        if "parse" not in res_json:
            print(f"❌ Page absente : {tournoi}")
            continue

        html = res_json["parse"]["text"]["*"]
        df = parse_champion_table(html, tournoi)

        if df is None or df.empty:
            continue

        # 📁 Export CSV
        filename = f"exports_lec_champions/{tournoi.replace('/', '_')}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        print(f"✔ Sauvegardé : {filename}")

        # ⏱️ Pause pour éviter surcharge serveur
        time.sleep(0.5)

    except Exception as e:
        print(f"Erreur pour {tournoi} : {e}")

print("🏁 Scraping terminé")

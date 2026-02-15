from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
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
# Dossier de sortie
os.makedirs("exports_lec", exist_ok=True)

driver = webdriver.Chrome()
all_data = {}
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

        # ✔ gestion des pages absentes
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
            cells = [c.get_text(strip=True) for c in row.select("th, td")]
            if cells:
                data.append(cells)

        df = pd.DataFrame(data)
        df = df.iloc[4:]
        df.columns = [ "ID", "Name", "Games", "Wins", "Loses", "Winrate", "Kills/Game", "Deaths/Game", "Assists/Game", "KDA", "CS/Game", "CS/Min", "Vision/Game", "Vision/Min", "Golds/Game", "Golds/Min", "Damage/Game", "Damage/Min", "Kill Participation", "Kill Shara", "Gold Share", "Nombre Champions", "Champs", ]

        # sauvegarde par feuille
        all_data[tournoi.replace("/", "_")] = df

    except Exception as e:
        print(f"Erreur pour {tournoi} : {e}")

# ✔ Export Excel multi-feuilles
with pd.ExcelWriter("stats_lec.xlsx", engine="openpyxl") as writer:
    for sheet, df in all_data.items():
        df.to_excel(writer, sheet_name=sheet[:31], index=False)
        worksheet = writer.sheets[sheet[:31]] 
        for column in worksheet.columns: 
            max_length = 0 
            column_letter = column[0].column_letter 
            for cell in column: 
                if cell.value: 
                    max_length = max(max_length, len(str(cell.value))) 
            worksheet.column_dimensions[column_letter].width = max_length + 2

print("✔ Terminé")
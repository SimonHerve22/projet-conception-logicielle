from bs4 import BeautifulSoup
import pandas as pd


# Charger le fichier HTML
with open("demofile.html", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Trouver le tableau principal contenant les statistiques des joueurs
main_table = soup.find("table", class_="wikitable")

# Extraire les lignes du tableau
rows = main_table.find_all("tr")

# Initialiser une liste pour stocker les données
player_data = []

# Parcourir chaque ligne
for row in rows:
    cols = row.find_all("td")
    cols = [col.text.strip() for col in cols]

    # Filtrer les lignes contenant des statistiques de joueurs
    if len(cols) > 5 and any(char.isdigit() for char in " ".join(cols)):
        player_data.append(cols)

# Convertir en DataFrame pour une meilleure visualisation
df = pd.DataFrame(player_data)

df.columns = [
    "id",
    "name",
    "game",
    "win",
    "lose",
    "wr",
    "k",
    "d",
    "a",
    "kda",
    "cs",
    "cs/m",
    "vs",
    "vs/m",
    "g",
    "g/m",
    "dgm",
    "dgm/m",
    "kpar",
    "ks",
    "gs",
    "cp",
    "jsp",
]

print(df.head())

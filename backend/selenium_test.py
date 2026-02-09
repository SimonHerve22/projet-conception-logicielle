from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


liste_tournois = ['EU_LCS/Season_3/Spring_Season', 'EU_LCS/Season_3/Spring_Playoffs', 'EU_LCS/Season_3/Summer_Season', 'EU_LCS/Season_3/Summer_Playoffs',
'EU_LCS/2014_Season/Spring_Season', 'EU_LCS/2014_Season/Spring_Playoffs', 'EU_LCS/2014_Season/Summer_Season', 'EU_LCS/2014_Season/Summer_Playoffs',
'EU_LCS/2015_Season/Spring_Season', 'EU_LCS/2015_Season/Spring_Playoffs', 'EU_LCS/2015_Season/Summer_Season', 'EU_LCS/2015_Season/Summer_Playoffs',
'EU_LCS/2016_Season/Spring_Season', 'EU_LCS/2016_Season/Spring_Playoffs', 'EU_LCS/2016_Season/Summer_Season', 'EU_LCS/2016_Season/Summer_Playoffs',
'EU_LCS/2017_Season/Spring_Season', 'EU_LCS/2017_Season/Spring_Playoffs', 'EU_LCS/2017_Season/Summer_Season', 'EU_LCS/2017_Season/Summer_Playoffs',
'EU_LCS/2018_Season/Spring_Season', 'EU_LCS/2018_Season/Spring_Playoffs', 'EU_LCS/2018_Season/Summer_Season', 'EU_LCS/2018_Season/Summer_Playoffs',
'LEC/2019_Season/Spring_Season', 'LEC/2019_Season/Spring_Playoffs', 'LEC/2019_Season/Summer_Season', 'LEC/2019_Season/Summer_Playoffs',
'LEC/2020_Season/Spring_Season', 'LEC/2020_Season/Spring_Playoffs', 'LEC/2020_Season/Summer_Season', 'LEC/2020_Season/Summer_Playoffs',
'LEC/2021_Season/Spring_Season', 'LEC/2021_Season/Spring_Playoffs', 'LEC/2021_Season/Summer_Season', 'LEC/2021_Season/Summer_Playoffs',
'LEC/2022_Season/Spring_Season', 'LEC/2022_Season/Spring_Playoffs', 'LEC/2022_Season/Summer_Season', 'LEC/2022_Season/Summer_Playoffs',
'LEC/2023_Season/Winter_Season', 'LEC/2023_Season/Winter_Groups', 'LEC/2023_Season/Winter_Playoffs',
'LEC/2023_Season/Spring_Season', 'LEC/2023_Season/Spring_Groups', 'LEC/2023_Season/Spring_Playoffs',
'LEC/2023_Season/Summer_Season', 'LEC/2023_Season/Summer_Groups', 'LEC/2023_Season/Summer_Playoffs',
'LEC/2024_Season/Winter_Season', 'LEC/2024_Season/Winter_Playoffs',
'LEC/2024_Season/Spring_Season', 'LEC/2024_Season/Spring_Playoffs',
'LEC/2024_Season/Summer_Season', 'LEC/2024_Season/Summer_Playoffs',
'LEC/2025_Season/Winter_Season', 'LEC/2025_Season/Winter_Playoffs',
'LEC/2025_Season/Spring_Season', 'LEC/2025_Season/Spring_Playoffs',
'LEC/2025_Season/Summer_Season', 'LEC/2025_Season/Summer_Playoffs',
'LEC/2026_Season/Versus_Season', 'LEC/2026_Season/Versus_Playoffs']

liste_pages = ['Overview', 'Team Rosters', 'Picks & Bans', 'Match History', 'Champion Stats', 'Player Stats']

driver = webdriver.Chrome()
driver.get(
"https://lol.fandom.com/wiki/LEC/2026_Season/Versus_Season/Player_Statistics"
)
driver.implicitly_wait(10)

table_html = driver.find_element(
By.CSS_SELECTOR, "#mw-content-text table.wikitable"
).get_attribute("outerHTML")

driver.quit()

soup = BeautifulSoup(table_html, "html.parser")

rows = soup.find_all("tr")

data = []
for row in rows[1:]: # skip header
    cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
if cells:
    data.append(cells)

# Exemple : afficher la première ligne joueur
print(data[0])

print(data)

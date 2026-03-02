# infrastructure/leaguepedia_player_scraper.py


from bs4 import BeautifulSoup
from business_object.joueur_stat import PlayerStat
import requests


class LeaguepediaPlayerScraper:
    BASE_URL = "https://lol.fandom.com/api.php"

    def fetch_stats(self, tournoi_path: str) -> list[PlayerStat]:
        html = self._fetch_html(tournoi_path)
        return self._parse_html(html, tournoi_path)

    # -----------------------------
    # 🔽 API CALL
    # -----------------------------

    def _fetch_html(self, tournoi_path: str) -> str:
        params = {
            "action": "parse",
            "page": f"{tournoi_path}/Player_Statistics",
            "prop": "text",
            "format": "json",
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "parse" not in data:
            raise ValueError(f"Page introuvable : {tournoi_path}")

        return data["parse"]["text"]["*"]

    # -----------------------------
    # 🔽 PARSING
    # -----------------------------

    def _parse_html(self, html: str, tournoi_path: str) -> list[PlayerStat]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("table.wikitable")

        if table is None:
            raise ValueError("Table wikitable introuvable")

        rows = table.select("tr")[1:]
        stats: list[PlayerStat] = []

        for row in rows:
            cols = row.select("th, td")

            if len(cols) < 23:
                continue  # ignore lignes parasites

            try:
                equipe = self._extract_team_name(cols[0])
                name = cols[1].get_text(strip=True)

                games = self._to_int(cols[2].get_text())
                wins = self._to_int(cols[3].get_text())
                losses = self._to_int(cols[4].get_text())
                winrate = self._to_float(cols[5].get_text())
                kda = self._to_float(cols[9].get_text())
                kill_participation = self._to_float(cols[18].get_text())
                main_champion = self._extract_first_champion(cols[-1])

                stat = PlayerStat(
                    tournoi=tournoi_path,
                    equipe=equipe,
                    name=name,
                    games=games,
                    wins=wins,
                    losses=losses,
                    winrate=winrate,
                    kda=kda,
                    kill_participation=kill_participation,
                    main_champion=main_champion,
                )

                stats.append(stat)

            except Exception:
                continue

        return stats

    # -----------------------------
    # 🔽 HELPERS
    # -----------------------------

    def _extract_team_name(self, cell):
        link = cell.find("a")
        if link and link.get("title"):
            return link["title"]

        img = cell.find("img")
        if img and img.get("alt"):
            return img["alt"]

        return cell.get_text(strip=True)

    def _extract_first_champion(self, cell):
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

    def _to_int(self, value: str) -> int:
        return int(value.strip().replace("%", "").replace(",", ""))

    def _to_float(self, value: str) -> float:
        return float(value.strip().replace("%", "").replace(",", ""))

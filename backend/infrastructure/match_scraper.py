from bs4 import BeautifulSoup
from business_object.match import Match
import requests


class LeaguepediaMatchScraper:
    BASE_URL = "https://lol.fandom.com/api.php"

    # --------------------------------------------------
    # 🔽 PUBLIC API
    # --------------------------------------------------

    def fetch(self, tournoi_path: str) -> list[Match]:
        html = self._fetch_html(tournoi_path)
        return self._parse_html(html, tournoi_path)

    # --------------------------------------------------
    # 🔽 API CALL
    # --------------------------------------------------

    def _fetch_html(self, tournoi_path: str) -> str:
        params = {
            "action": "parse",
            "page": f"{tournoi_path}/Match_History",
            "prop": "text",
            "format": "json",
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "parse" not in data:
            raise ValueError(f"Page Match_History introuvable : {tournoi_path}")

        return data["parse"]["text"]["*"]

    # --------------------------------------------------
    # 🔽 PARSING
    # --------------------------------------------------

    def _parse_html(self, html: str, tournoi_path: str) -> list[Match]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("table.mhgame")

        if table is None:
            raise ValueError("Table mhgame introuvable")

        rows = table.select("tbody tr")
        matches: list[Match] = []

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 5:
                continue

            try:
                date = cols[0].get_text(strip=True)
                patch = cols[1].get_text(strip=True)
                blue = self._extract_team(cols[2])
                red = self._extract_team(cols[3])
                winner = self._extract_team(cols[4])

                matches.append(
                    Match(
                        tournoi=tournoi_path,
                        date=date,
                        patch=patch,
                        blue_team=blue,
                        red_team=red,
                        winner=winner,
                    )
                )

            except Exception:
                continue

        return matches

    # --------------------------------------------------
    # 🔽 HELPERS
    # --------------------------------------------------

    def _extract_team(self, cell):
        link = cell.find("a")
        if link and link.get("title"):
            return link["title"]

        img = cell.find("img")
        if img and img.get("alt"):
            return img["alt"]

        return cell.get_text(strip=True)

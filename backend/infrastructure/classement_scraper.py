from bs4 import BeautifulSoup
from business_object.classement import (
    PlayoffResult,
    RegularSeasonStanding,
)
import requests


class LeaguepediaStandingsScraper:
    BASE_URL = "https://lol.fandom.com/api.php"

    # --------------------------------------------------
    # 🔽 PUBLIC API
    # --------------------------------------------------

    def fetch(self, page_path: str):
        html = self._fetch_html(page_path)
        return self._parse_html(html, page_path)

    # --------------------------------------------------
    # 🔽 API CALL
    # --------------------------------------------------

    def _fetch_html(self, page_path: str) -> str:
        params = {
            "action": "parse",
            "page": page_path,
            "prop": "text",
            "format": "json",
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "parse" not in data:
            raise ValueError(f"Page introuvable : {page_path}")

        return data["parse"]["text"]["*"]

    # --------------------------------------------------
    # 🔽 PARSING
    # --------------------------------------------------

    def _parse_html(self, html: str, page_path: str):
        soup = BeautifulSoup(html, "html.parser")

        if self._is_playoff(page_path):
            return self._parse_playoffs(soup, page_path)
        else:
            return self._parse_regular_season(soup, page_path)

    # --------------------------------------------------
    # 🔽 REGULAR SEASON
    # --------------------------------------------------

    def _parse_regular_season(self, soup, page_path: str):
        table = soup.select_one("table.standings")

        if table is None:
            raise ValueError("Table standings introuvable")

        rows = table.find_all("tr")
        results: list[RegularSeasonStanding] = []

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 5:
                continue

            try:
                rang = self._to_int(cols[0].get_text())
                equipe = self._extract_team_name(cols[1])
                score = cols[2].get_text(strip=True)
                winrate = self._to_float(cols[3].get_text())
                streak = cols[4].get_text(strip=True)

                results.append(
                    RegularSeasonStanding(
                        tournoi=page_path,
                        rang=rang,
                        equipe=equipe,
                        score=score,
                        winrate=winrate,
                        streak=streak,
                    )
                )

            except Exception:
                continue

        return results

    # --------------------------------------------------
    # 🔽 PLAYOFFS
    # --------------------------------------------------

    def _parse_playoffs(self, soup, page_path: str):
        cell = soup.find("td", class_="tournament-results-team")

        if cell is None:
            raise ValueError("Table playoffs introuvable")

        table = cell.find_parent("table")
        rows = table.find_all("tr")

        results: list[PlayoffResult] = []

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            try:
                place = cols[0].get_text(strip=True)
                qualification = cols[1].get_text(strip=True)
                equipe = self._extract_team_name(cols[2])

                results.append(
                    PlayoffResult(
                        tournoi=page_path,
                        place=place,
                        qualification=qualification,
                        equipe=equipe,
                    )
                )

            except Exception:
                continue

        return results

    # --------------------------------------------------
    # 🔽 HELPERS
    # --------------------------------------------------

    def _is_playoff(self, page_path: str) -> bool:
        return "Playoffs" in page_path

    def _extract_team_name(self, cell):
        team_span = cell.select_one(".teamname")
        if team_span:
            return team_span.get_text(strip=True)

        link = cell.find("a")
        if link and link.get("title"):
            return link["title"]

        return cell.get_text(strip=True)

    def _to_int(self, value: str) -> int:
        return int(value.strip().replace("%", "").replace(",", ""))

    def _to_float(self, value: str) -> float:
        return float(value.strip().replace("%", "").replace(",", ""))

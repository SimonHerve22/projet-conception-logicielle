from bs4 import BeautifulSoup
import fandom


class LeagueAPI:
    def __init__(self, wiki: str = "lol"):
        fandom.set_wiki(wiki)

    @staticmethod
    def get_team_names() -> dict[str, list[str]]:
        """
        Retourne les noms exacts des équipes par ligue (LEC / LCK / LPL)
        """
        return {
            "LEC": [
                "G2 Esports",
                "Fnatic",
                "Team Vitality",
                "MAD Lions",
                "Team BDS",
                "SK Gaming",
                "Rogue",
                "KOI",
                "GIANTX",
                "Team Heretics",
            ],
            "LCK": [
                "T1",
                "Gen.G",
                "Hanwha Life Esports",
                "Dplus KIA",
                "KT Rolster",
                "DRX",
                "Kwangdong Freecs",
                "Nongshim RedForce",
                "OKSavingsBank BRION",
                "FearX",
            ],
            "LPL": [
                "JD Gaming",
                "Top Esports",
                "Bilibili Gaming",
                "FunPlus Phoenix",
                "Invictus Gaming",
                "Weibo Gaming",
                "EDward Gaming",
                "LNG Esports",
                "Royal Never Give Up",
                "Anyone's Legend",
            ],
        }

    def get_team_page_html(self, team_name: str) -> str:
        """
        Récupère le HTML de la page d'une équipe
        """
        page = fandom.page(title=team_name)
        return page.html

    def get_team_info(self, team_name: str) -> dict:
        """
        Retourne les infos principales d'une équipe
        """
        html = self.get_team_page_html(team_name)
        soup = BeautifulSoup(html, "html.parser")

        info = {}

        infobox = soup.find("aside", class_="portable-infobox")
        if not infobox:
            raise ValueError("Infobox équipe non trouvée")

        for item in infobox.find_all("section", class_="pi-item"):
            label = item.find("h3")
            value = item.find("div")

            if label and value:
                info[label.text.strip()] = value.text.strip()

        return info

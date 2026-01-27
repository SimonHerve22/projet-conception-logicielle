import argparse

from bs4 import BeautifulSoup
import fandom
import pandas as pd


# ------------------------------------------------------------
# DATA FETCH
# ------------------------------------------------------------

ALLOWED_LEAGUES = {"LEC", "LPL", "LCK", "LCK_CL"}
ALLOWED_SPLITS = {
    "Spring_Season",
    "Spring_Playoffs",
    "Summer_Season",
    "Summer_Playoffs",
}
ALLOWED_YEARS = range(2020, 2027)


def parse_cli_arguments() -> argparse.Namespace:
    """
    Parse les arguments de la ligne de commande
    """
    parser = argparse.ArgumentParser(
        description="Extraction des statistiques joueurs depuis Leaguepedia"
    )

    parser.add_argument(
        "--league",
        required=True,
        choices=sorted(ALLOWED_LEAGUES),
        help="Ligue (ex: LEC, LPL, LCK, LCK_CL)",
    )

    parser.add_argument(
        "--year",
        required=True,
        type=int,
        choices=ALLOWED_YEARS,
        help="Année (2020–2026)",
    )

    parser.add_argument(
        "--split",
        required=True,
        choices=sorted(ALLOWED_SPLITS),
        help="Split de la saison",
    )

    return parser.parse_args()


def build_player_stats_path(
    league: str,
    year: int,
    split: str,
) -> str:
    """
    Construit le chemin Leaguepedia vers les statistiques joueurs
    """
    if league not in ALLOWED_LEAGUES:
        raise ValueError(f"Ligue invalide : {league}")

    if year not in ALLOWED_YEARS:
        raise ValueError(f"Année invalide : {year}")

    if split not in ALLOWED_SPLITS:
        raise ValueError(f"Split invalide : {split}")

    return f"{league}/{year}_Season/{split}/Player_Statistics"


def get_player_stats_data_as_html(
    league: str,
    year: int,
    split: str,
) -> str:
    """
    Récupère le HTML de la page Leaguepedia des statistiques joueurs
    """
    fandom.set_wiki("lol")

    path = build_player_stats_path(league, year, split)
    player_stats = fandom.page(title=path)

    return player_stats.html


# ------------------------------------------------------------
# PARSING
# ------------------------------------------------------------


def parse_lec_player_stats(html_content: str) -> pd.DataFrame:
    """
    Parse les statistiques des joueurs LEC depuis Leaguepedia

    Args:
        html_content (str): HTML brut de la page

    Returns:
        pd.DataFrame: DataFrame contenant toutes les statistiques des joueurs
    """
    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find("table", class_=["wikitable", "sortable", "spstats"])
    if not table:
        raise ValueError("Tableau de statistiques non trouvé dans le HTML")

    # En-têtes attendus (ordre Leaguepedia)
    clean_headers = [
        "Team",
        "Player",
        "Games",
        "Wins",
        "Losses",
        "Win Rate",
        "Kills",
        "Deaths",
        "Assists",
        "KDA",
        "CS",
        "CS/M",
        "Vision Score",
        "VS/M",
        "Gold",
        "Gold/M",
        "Damage",
        "DMG/M",
        "Kill Participation",
        "Kill Share",
        "Gold Share",
        "Champions Played",
        "Champion Pool",
    ]

    rows_data = []
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        cells = row.find_all("td")

        if not cells or len(cells) < 5:
            continue

        row_data = []

        for i, cell in enumerate(cells):
            # Team
            if i == 0:
                team_link = cell.find("a")
                row_data.append(team_link.get("title", "") if team_link else "")

            # Player
            elif i == 1:
                player_link = cell.find("a")
                row_data.append(
                    player_link.get_text(strip=True)
                    if player_link
                    else cell.get_text(strip=True)
                )

            # Champion Pool (images)
            elif i == len(cells) - 1:
                champions = [
                    img.get("title", "")
                    for img in cell.find_all("span", class_="sprite")
                ]
                row_data.append(", ".join(champions) if champions else "")

            # Autres stats
            else:
                text = cell.get_text(strip=True)
                text = text.replace("\u200b", "").replace("\xa0", "")
                row_data.append(text)

        if len(row_data) > 5:
            rows_data.append(row_data)

    df = pd.DataFrame(rows_data, columns=clean_headers[: len(rows_data[0])])

    return df


# ------------------------------------------------------------
# CLEANING
# ------------------------------------------------------------


def clean_and_convert_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et convertit les colonnes numériques
    """
    df_clean = df.copy()

    numeric_cols = {
        "Games": int,
        "Wins": int,
        "Losses": int,
        "Kills": float,
        "Deaths": float,
        "Assists": float,
        "KDA": float,
        "CS": float,
        "CS/M": float,
        "Vision Score": float,
        "VS/M": float,
        "Gold": float,
        "Gold/M": float,
        "Damage": float,
        "DMG/M": float,
        "Champions Played": int,
    }

    percent_cols = [
        "Win Rate",
        "Kill Participation",
        "Kill Share",
        "Gold Share",
    ]

    for col, dtype in numeric_cols.items():
        if col in df_clean.columns:
            try:
                cleaned = (
                    df_clean[col]
                    .astype(str)
                    .str.replace(",", "")
                    .str.replace("k", "000")
                )
                df_clean[col] = pd.to_numeric(cleaned, errors="coerce").astype(dtype)
            except Exception as e:
                print(f"⚠️ Erreur conversion {col}: {e}")

    for col in percent_cols:
        if col in df_clean.columns:
            try:
                cleaned = df_clean[col].astype(str).str.replace("%", "")
                df_clean[col] = pd.to_numeric(cleaned, errors="coerce")
            except Exception as e:
                print(f"⚠️ Erreur conversion {col}: {e}")

    return df_clean


# ------------------------------------------------------------
# ANALYTICS
# ------------------------------------------------------------


def generate_summary_stats(df: pd.DataFrame) -> None:
    """
    Génère des statistiques récapitulatives
    """
    print("\n" + "=" * 70)
    print("📊 STATISTIQUES RÉCAPITULATIVES - LEC 2026 VERSUS SEASON")
    print("=" * 70 + "\n")

    print(f"🎮 Nombre total de joueurs: {len(df)}")
    print(f"🏆 Nombre d'équipes: {df['Team'].nunique()}")
    print(f"🎯 Total de parties jouées: {df['Games'].sum()}\n")

    print("─" * 70)
    print("TOP 5 JOUEURS PAR STATISTIQUE")
    print("─" * 70 + "\n")

    print("Meilleur KDA :")
    for _, row in df.nlargest(5, "KDA").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['KDA']:.2f}")

    print("\nPlus de kills par partie :")
    for _, row in df.nlargest(5, "Kills").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['Kills']:.2f}")

    print("\nPlus d'assistances par partie :")
    for _, row in df.nlargest(5, "Assists").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['Assists']:.2f}")

    print("\nPlus de farm par minute :")
    for _, row in df.nlargest(5, "CS/M").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['CS/M']:.2f}")

    print("\nPlus d'or par minute :")
    for _, row in df.nlargest(5, "Gold/M").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['Gold/M']:.2f}")

    print("\nPlus de dégâts par minute :")
    for _, row in df.nlargest(5, "DMG/M").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['DMG/M']:.2f}")

    print("\nPlus de vision par minute :")
    for _, row in df.nlargest(5, "VS/M").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['VS/M']:.2f}")

    print("\nPlus de participation aux kills dans son équipe :")
    for _, row in df.nlargest(5, "Kill Participation").iterrows():
        print(
            f" {row['Player']:15} ({row['Team']:20}) - {row['Kill Participation']:.1f}"
        )

    print("\nPlus grande partie des golds de son équipe :")
    for _, row in df.nlargest(5, "Gold Share").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['Gold Share']:.1f}")

    print("\nPlus grand nombre de personnages joués :")
    for _, row in df.nlargest(5, "Champions Played").iterrows():
        print(f" {row['Player']:15} ({row['Team']:20}) - {row['Champions Played']:.0f}")

    print("\n" + "=" * 70 + "\n")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        args = parse_cli_arguments()

        league = args.league
        year = args.year
        split = args.split

        print(f"🚀 Parsing {league} {year} {split} - Leaguepedia\n")

        html_content = get_player_stats_data_as_html(
            league=league,
            year=year,
            split=split,
        )

        df_raw = parse_lec_player_stats(html_content)
        print(f"✅ {len(df_raw)} joueurs trouvés\n")

        print("🔧 Nettoyage et conversion des données...")
        df_clean = clean_and_convert_stats(df_raw)

        generate_summary_stats(df_clean)

        output_file = f"{league.lower()}_{year}_{split.lower()}_player_stats.csv"

        df_clean.to_csv(output_file, index=False, encoding="utf-8")
        print(f"💾 Export global : {output_file}")

        print("\n✨ Terminé avec succès !\n")

    except Exception as e:
        import traceback

        print(f"❌ Erreur: {e}")
        traceback.print_exc()

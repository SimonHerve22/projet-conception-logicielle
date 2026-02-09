import argparse
import sys

import pandas as pd
import requests


# ------------------------------------------------------------
# CONFIGURATION
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
    parser = argparse.ArgumentParser(
        description="Extraction des statistiques via API Cargo Leaguepedia"
    )
    parser.add_argument("--league", required=True, choices=sorted(ALLOWED_LEAGUES))
    parser.add_argument("--year", required=True, type=int, choices=ALLOWED_YEARS)
    parser.add_argument("--split", required=True, choices=sorted(ALLOWED_SPLITS))
    return parser.parse_args()


# ------------------------------------------------------------
# DATA FETCH (API CARGO)
# ------------------------------------------------------------


def fetch_player_stats_cargo(league: str, year: int, split: str) -> pd.DataFrame:
    """
    Interroge l'API Cargo de Leaguepedia pour obtenir les stats propres.
    """
    url = "https://lol.fandom.com/api.php"

    # Transformation du split pour le format Cargo (ex: Spring_Playoffs -> Spring Playoffs)
    split_clean = split.replace("_", " ")
    tournament_name = f"{league}/{year} Season/{split_clean}"

    # On définit les colonnes que l'on veut récupérer
    fields = [
        "Player",
        "Team",
        "Games",
        "Wins",
        "Losses",
        "Kills",
        "Deaths",
        "Assists",
        "KDA",
        "CS",
        "CSM",
        "Gold",
        "GPM",
        "Damage",
        "DPM",
        "VSPM",
        "KillParticipation",
        "KillShare",
        "GoldShare",
        "ChampionsPlayed",
    ]

    params = {
        "action": "cargoquery",
        "format": "json",
        "tables": "PlayerStats",
        "fields": ",".join(fields),
        "where": f"Tournament='{tournament_name}'",
        "limit": "500",
    }

    print(f"📡 Requête API pour : {tournament_name}...")

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "cargoquery" not in data or not data["cargoquery"]:
        print(f"❌ Aucune donnée trouvée pour {tournament_name}.")
        print(
            "Note : Vérifiez si le tournoi a déjà commencé et si les stats sont publiées."
        )
        sys.exit(1)

    # Extraction des données JSON vers une liste de dictionnaires
    rows = [item["title"] for item in data["cargoquery"]]
    df = pd.DataFrame(rows)

    # Renommage pour rester cohérent avec ton ancien code
    rename_map = {
        "CSM": "CS/M",
        "GPM": "Gold/M",
        "DPM": "DMG/M",
        "VSPM": "VS/M",
        "KillParticipation": "Kill Participation",
        "KillShare": "Kill Share",
        "GoldShare": "Gold Share",
        "ChampionsPlayed": "Champions Played",
    }
    df.rename(columns=rename_map, inplace=True)

    return df


# ------------------------------------------------------------
# CLEANING
# ------------------------------------------------------------


def clean_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les colonnes de l'API (qui arrivent en string) vers les bons formats.
    """
    df_clean = df.copy()

    # Colonnes numériques classiques
    numeric_cols = [
        "Games",
        "Wins",
        "Losses",
        "Kills",
        "Deaths",
        "Assists",
        "KDA",
        "CS",
        "CS/M",
        "Gold",
        "Gold/M",
        "Damage",
        "DMG/M",
        "VS/M",
        "Champions Played",
    ]

    # Colonnes de pourcentages (souvent envoyées comme "0.72" pour 72%)
    percent_cols = ["Kill Participation", "Kill Share", "Gold Share"]

    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0)

    for col in percent_cols:
        if col in df_clean.columns:
            # L'API Cargo donne souvent les ratios en 0-1 (ex: 0.65 pour 65%)
            # On multiplie par 100 pour garder ton format d'origine
            df_clean[col] = (
                pd.to_numeric(df_clean[col], errors="coerce").fillna(0) * 100
            )

    return df_clean


# ------------------------------------------------------------
# ANALYTICS (Identique à ton code)
# ------------------------------------------------------------


def generate_summary_stats(df: pd.DataFrame, league, year, split) -> None:
    print("\n" + "=" * 70)
    print(f"📊 STATISTIQUES RÉCAPITULATIVES - {league} {year} {split}")
    print("=" * 70 + "\n")

    print(f"🎮 Nombre total de joueurs: {len(df)}")
    print(f"🏆 Nombre d'équipes: {df['Team'].nunique()}")
    print(
        f"🎯 Total de parties jouées: {int(df['Games'].sum() / 10)}\n"
    )  # Divisé par 10 car 10 joueurs par match

    metrics = [
        ("Meilleur KDA", "KDA", ".2f"),
        ("Plus de kills par partie", "Kills", ".2f"),
        ("Plus d'assistances par partie", "Assists", ".2f"),
        ("Plus de farm par minute", "CS/M", ".2f"),
        ("Plus de dégâts par minute", "DMG/M", ".2f"),
        ("Participation aux kills (%)", "Kill Participation", ".1f"),
    ]

    for label, col, fmt in metrics:
        print(f"--- {label} ---")
        top5 = df.nlargest(5, col)
        for _, row in top5.iterrows():
            print(f" {row['Player']:15} ({row['Team']:15}) - {row[col]:{fmt}}")
        print()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        args = parse_cli_arguments()

        # 1. Fetch
        df_raw = fetch_player_stats_cargo(args.league, args.year, args.split)

        # 2. Clean
        df_clean = clean_stats(df_raw)

        # 3. Analytics
        generate_summary_stats(df_clean, args.league, args.year, args.split)

        # 4. Export
        output_file = (
            f"{args.league.lower()}_{args.year}_{args.split.lower()}_stats.csv"
        )
        df_clean.to_csv(output_file, index=False, encoding="utf-8")
        print(f"💾 Export : {output_file}")
        print("\n✨ Terminé avec succès !")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")

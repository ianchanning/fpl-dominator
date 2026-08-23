import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

TLA_TO_CLUB: Dict[str, str] = {
    "ARS": "Arsenal",
    "AVL": "Aston Villa",
    "BOU": "Bournemouth",
    "BRE": "Brentford",
    "BHA": "Brighton and Hove Albion",
    "CHE": "Chelsea",
    "CRY": "Crystal Palace",
    "EVE": "Everton",
    "FUL": "Fulham",
    "LEE": "Leeds United",
    "LIV": "Liverpool",
    "MCI": "Manchester City",
    "MUN": "Manchester United",
    "NEW": "Newcastle United",
    "NFO": "Nottingham Forest",
    "SUN": "Sunderland",
    "TOT": "Tottenham Hotspur",
    "COV": "Coventry City",
    "HUL": "Hull City",
    "IPS": "Ipswich Town",
}

PROMOTED_FALLBACKS: Dict[str, Dict[str, str]] = {
    "Coventry City": {
        "Penalties": "Simms, Wright",
        "Direct Free Kicks": "Rudoni, Torp",
        "Corners & Indirect Free Kicks": "Rudoni, Torp",
    },
    "Hull City": {
        "Penalties": "Gelhardt, Pedro",
        "Direct Free Kicks": "Slater, Mehlem",
        "Corners & Indirect Free Kicks": "Mehlem, Giles",
    },
    "Ipswich Town": {
        "Penalties": "Chaplin, Broadhead",
        "Direct Free Kicks": "Davis, Morsy",
        "Corners & Indirect Free Kicks": "Davis, Morsy",
    },
}


def clean_player_surname(raw_name_cell: str) -> str:
    """Extracts a clean surname suitable for joins and set piece tracking."""
    lines = [line.strip() for line in raw_name_cell.strip().split("\n") if line.strip()]
    if not lines:
        return ""
    name = lines[0]
    # Remove parenthetical details like (Reece), (Enzo), (Zach)
    clean = re.sub(r"\s*\(.*?\)", "", name).strip()
    return clean


def parse_set_pieces_html(html_path: str) -> pd.DataFrame:
    """
    Parses a set pieces HTML dump into a detailed statistical DataFrame.
    """
    print(f"--- [SET PIECE RITUAL] Parsing Set Piece Table from '{html_path}' ---")
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Set piece HTML file not found at '{html_path}'")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    table = soup.find("table")
    if not table:
        raise ValueError(f"No table element found in '{html_path}'")

    thead = table.find("thead")
    header_rows = thead.find_all("tr") if thead else []
    th_row = header_rows[1] if len(header_rows) > 1 else (header_rows[0] if header_rows else [])
    th_tags = th_row.find_all("th") if th_row else []

    col_names = []
    for th in th_tags:
        stat = th.get("data-stat")
        label = th.text.strip()
        col_names.append(stat if stat else (label if label else "Icon"))

    rows = []
    tbody = table.find("tbody")
    if tbody:
        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            if not tds:
                continue
            row_dict = {}
            for i, td in enumerate(tds):
                col = col_names[i] if i < len(col_names) else f"col_{i}"
                if col == "Name":
                    row_dict["Surname"] = clean_player_surname(td.text)
                    row_dict["Full_Info"] = " ".join(td.text.split())
                else:
                    row_dict[col] = td.text.strip()
            rows.append(row_dict)

    df = pd.DataFrame(rows)
    print(f"[+] Extracted {len(df)} player records from set piece HTML.")

    # Numeric conversions
    numeric_cols = [
        "Appearances", "Time Played - Exact", "Goals From Penalties", "Goals From Set Plays",
        "Headed Goal Attempts From Set Plays", "Shots From Set Plays", "Corners",
        "Corners - Successful", "Crosses From Free Kick", "Crosses From Free Kick - Successful"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Per-90 and Potency Metrics
    df["Mins"] = df.get("Time Played - Exact", 0)
    df["Mins_90s"] = (df["Mins"] / 90.0).clip(lower=0.01)
    df["Corners_per_90"] = (df["Corners"] / df["Mins_90s"]).round(2)
    df["FK_Crosses_per_90"] = (df["Crosses From Free Kick"] / df["Mins_90s"]).round(2)
    df["SetPieceShots_per_90"] = (df["Shots From Set Plays"] / df["Mins_90s"]).round(2)

    df["Club"] = df["Team"].map(TLA_TO_CLUB).fillna(df["Team"])
    return df


def generate_empirical_set_pieces_csv(
    detailed_df: pd.DataFrame,
    output_path: str = "set_pieces.csv",
    save_detailed_path: Optional[str] = "archive/2025-26/set_pieces_detailed_2025_26.csv"
) -> pd.DataFrame:
    """
    Synthesizes empirical volume into a ranked set_pieces.csv table.
    """
    if save_detailed_path:
        os.makedirs(os.path.dirname(save_detailed_path), exist_ok=True)
        detailed_df.to_csv(save_detailed_path, index=False)
        print(f"[+] Saved detailed set pieces dataset to '{save_detailed_path}'.")

    empirical_clubs = []

    for tla, club_name in sorted(TLA_TO_CLUB.items()):
        # Check if promoted club fallback
        if club_name in PROMOTED_FALLBACKS and detailed_df[detailed_df["Team"] == tla].empty:
            empirical_clubs.append({
                "Club": club_name,
                "Penalties": PROMOTED_FALLBACKS[club_name]["Penalties"],
                "Direct Free Kicks": PROMOTED_FALLBACKS[club_name]["Direct Free Kicks"],
                "Corners & Indirect Free Kicks": PROMOTED_FALLBACKS[club_name]["Corners & Indirect Free Kicks"],
            })
            continue

        team_df = detailed_df[detailed_df["Team"] == tla]
        if team_df.empty:
            continue

        # Penalties: Rank by penalty goals, then shots from set plays
        pens = team_df[team_df["Goals From Penalties"] > 0].sort_values(
            by="Goals From Penalties", ascending=False
        )
        pen_takers = pens["Surname"].tolist()[:3]

        # Direct Free Kicks: Rank by crosses + shots
        fks = team_df[
            (team_df["Crosses From Free Kick"] > 0) | (team_df["Shots From Set Plays"] > 0)
        ].sort_values(
            by=["Crosses From Free Kick", "Shots From Set Plays"], ascending=[False, False]
        )
        fk_takers = fks["Surname"].tolist()[:3]

        # Corners: Rank by total corners taken
        cnrs = team_df[team_df["Corners"] > 0].sort_values(
            by="Corners", ascending=False
        )
        cnr_takers = cnrs["Surname"].tolist()[:4]

        empirical_clubs.append({
            "Club": club_name,
            "Penalties": ", ".join(pen_takers),
            "Direct Free Kicks": ", ".join(fk_takers),
            "Corners & Indirect Free Kicks": ", ".join(cnr_takers),
        })

    result_df = pd.DataFrame(empirical_clubs)
    result_df.to_csv(output_path, index=False)
    print(f"--- SUCCESS: Empirical set piece taker matrix forged at '{output_path}' ---")
    return result_df


if __name__ == "__main__":
    df = parse_set_pieces_html("archive/2025-26/set_pieces.html")
    generate_empirical_set_pieces_csv(df)

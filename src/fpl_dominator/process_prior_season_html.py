import os
import re
from typing import Dict, List, Optional

import pandas as pd
from bs4 import BeautifulSoup

POSITION_LOOKUP = {
    "Goalkeeper": "GKP",
    "Defender": "DEF",
    "Midfielder": "MID",
    "Forward": "FWD",
}

TLA_TO_FULL_NAME = {
    "ARS": "Arsenal",
    "AVL": "Aston Villa",
    "BHA": "Brighton",
    "BOU": "Bournemouth",
    "BRE": "Brentford",
    "BUR": "Burnley",
    "CHE": "Chelsea",
    "CRY": "Crystal Palace",
    "EVE": "Everton",
    "FUL": "Fulham",
    "LEE": "Leeds",
    "LIV": "Liverpool",
    "MCI": "Man City",
    "MUN": "Man Utd",
    "NEW": "Newcastle",
    "NFO": "Nott'm Forest",
    "SUN": "Sunderland",
    "TOT": "Spurs",
    "WHU": "West Ham",
    "WOL": "Wolves",
}

MANUAL_POSITION_FALLBACKS = {
    "Haaland": "FWD",
    "Semenyo": "MID",
    "Marc Guehi": "DEF",
    "Fernández (Enzo)": "MID",
}


def build_historical_position_map() -> Dict[str, str]:
    """Scans all historical gameweek CSVs in archive/ to build a
    fallback surname->position map."""
    pos_map: Dict[str, str] = {}
    for gw in range(38, 0, -1):
        for pos, fn in [
            ("GKP", "goalkeepers.csv"),
            ("DEF", "defenders.csv"),
            ("MID", "midfielders.csv"),
            ("FWD", "forwards.csv"),
        ]:
            path = f"archive/2025-26/gw{gw}/{fn}"
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path)
                    for _, row in df.iterrows():
                        surname = str(row["Surname"]).strip()
                        if surname not in pos_map:
                            pos_map[surname] = pos
                except Exception:
                    pass
    return pos_map


def parse_prior_season_html(
    html_path: str = "archive/2025-26/fpl_player_stats.html",
    output_csv_path: str = "archive/2025-26/fpl_player_stats_2025_26.csv",
) -> pd.DataFrame:
    """
    Parses the full-season aggregate player statistics HTML table from FPL/FFS.
    Handles dual header rows, metadata extraction, position mapping, and
    metric normalization.
    """
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Prior season HTML file not found at: {html_path}")

    print(f"[+] Loading prior season HTML from: {html_path}")
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    table = soup.find("table")
    if not table:
        raise ValueError(f"No <table> found in {html_path}")

    tbody = table.find("tbody")
    if not tbody:
        raise ValueError(f"No <tbody> found in table in {html_path}")

    rows = tbody.find_all("tr")
    print(f"[+] Found {len(rows)} player rows in table.")

    historical_pos_map = build_historical_position_map()
    records: List[Dict] = []

    def to_num(val_str: str, is_float: bool = False):
        val_str = val_str.replace(",", "").strip()
        if not val_str or val_str == "-":
            return 0.0 if is_float else 0
        try:
            return float(val_str) if is_float else int(val_str)
        except ValueError:
            return 0.0 if is_float else 0

    for row in rows:
        tds = row.find_all(["td", "th"])
        if len(tds) < 28:
            continue

        name_td = tds[1]
        a_tag = name_td.find("a")
        display_name = a_tag.text.strip() if a_tag else name_td.text.strip()
        full_name = a_tag.get("oldtitle", "").strip() if a_tag else ""
        slug = a_tag.get("href", "").strip() if a_tag else ""

        # Extract profile title metadata if rendered
        profile_div = name_td.find("div", class_="profile-title")
        pos_str: Optional[str] = None
        team_full_from_div: Optional[str] = None

        if profile_div:
            text = profile_div.text.strip()
            match = re.search(r"\(([^,]+),\s*([^)]+)\)", text)
            if match:
                team_full_from_div = match.group(1).strip()
                raw_pos = match.group(2).strip()
                pos_str = POSITION_LOOKUP.get(raw_pos, raw_pos)

        # Fallback position derivation if div was omitted
        if not pos_str:
            if display_name in MANUAL_POSITION_FALLBACKS:
                pos_str = MANUAL_POSITION_FALLBACKS[display_name]
            elif display_name in historical_pos_map:
                pos_str = historical_pos_map[display_name]
            else:
                pos_str = "MID"  # Default safe fallback

        team_tla = tds[2].text.strip()
        canonical_team = TLA_TO_FULL_NAME.get(team_tla, team_tla)
        team_full = team_full_from_div or canonical_team

        total_pts = to_num(tds[25].text)
        mins = to_num(tds[5].text)
        starts = to_num(tds[4].text)
        apps = to_num(tds[3].text)

        pts_per_90 = round(total_pts / (mins / 90.0), 2) if mins >= 90 else 0.0
        pts_per_start = to_num(tds[27].text, is_float=True)
        mins_per_pt = to_num(tds[26].text, is_float=True)

        records.append(
            {
                "Surname": display_name,
                "FullName": full_name,
                "Team_TLA": team_tla,
                "Team": canonical_team,
                "Team_Full": team_full,
                "Position": pos_str,
                "App": apps,
                "Starts": starts,
                "Mins": mins,
                "SubOn": to_num(tds[6].text),
                "SubOff": to_num(tds[7].text),
                "Goals": to_num(tds[10].text),
                "Assists": to_num(tds[11].text),
                "CleanSheets": to_num(tds[12].text),
                "GoalsConceded": to_num(tds[13].text),
                "OwnGoals": to_num(tds[14].text),
                "PenSaves": to_num(tds[15].text),
                "Saves": to_num(tds[16].text),
                "YellowCards": to_num(tds[17].text),
                "RedCards": to_num(tds[18].text),
                "Bonus": to_num(tds[23].text),
                "DoubleDigitHauls": to_num(tds[24].text),
                "TotalPoints": total_pts,
                "Mins_per_Pt": mins_per_pt,
                "Pts_per_Start": pts_per_start,
                "Pts_per_90": pts_per_90,
                "Slug": slug,
            }
        )

    df = pd.DataFrame(records)
    # Sort by TotalPoints descending
    df.sort_values(
        by=["TotalPoints", "Pts_per_90"], ascending=[False, False], inplace=True
    )

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"[+] Successfully forged prior season master database at: {output_csv_path}")
    print(f"[+] Total players processed: {len(df)}")
    return df


if __name__ == "__main__":
    parse_prior_season_html()

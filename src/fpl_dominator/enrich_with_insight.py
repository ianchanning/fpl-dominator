import os
import re
import sys
import unicodedata
from typing import Any, Dict, cast

import pandas as pd
import yaml

POSITION_PPM_BENCHMARKS = {
    "GKP": 24.0,  # e.g., £4.5m -> ~108 pts
    "DEF": 22.0,  # e.g., £4.5m -> ~99 pts, £6.0m -> ~132 pts
    "MID": 21.0,  # e.g., £5.5m -> ~115 pts, £10.0m -> ~210 pts
    "FWD": 20.0,  # e.g., £6.0m -> ~120 pts, £14.0m -> ~280 pts
}


def normalize_name(name: str) -> str:
    """Normalizes player names for robust cross-season joining."""
    if not isinstance(name, str):
        return ""
    # Strip diacritics / accents
    s = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    # Strip leading initials (e.g., 'A.Becker' -> 'Becker', 'M.Salah' -> 'Salah')
    s = re.sub(r"^[A-Z]\.\s*", "", s)
    # Strip parentheticals (e.g., 'Aina (Ola)' -> 'Aina')
    s = re.sub(r"\s*\(.*?\)", "", s)
    # Lowercase alphabetic only
    return re.sub(r"[^a-zA-Z]", "", s.lower())


def inject_bayesian_prior_baseline(
    players_df: pd.DataFrame,
    current_gw: int,
    prior_stats_path: str = "archive/2025-26/fpl_player_stats_2025_26.csv",
) -> pd.DataFrame:
    """
    Applies the Bayesian Cold Start & Season Transition Protocol (P4).
    Blends prior season performance truth with early season actuals via alpha_t decay.
    """
    # Compute decay parameter: alpha_t = max(0, 1 - (t - 1) / 5)
    if current_gw <= 0:
        alpha_t = 1.0
    elif current_gw >= 6:
        alpha_t = 0.0
    else:
        alpha_t = max(0.0, 1.0 - (current_gw - 1) / 5.0)

    if alpha_t <= 0.0:
        print(
            f"[+] Gameweek {current_gw} >= 6: Operating on 100% current season "
            f"performance (alpha=0.0)."
        )
        return players_df

    print(
        f"[+] Applying Bayesian Prior Cold Start "
        f"(GW{current_gw}, alpha={alpha_t:.2f})..."
    )
    if not os.path.exists(prior_stats_path):
        print(
            f"!!! WARNING: Prior season statistics not found at '{prior_stats_path}'. "
            f"Skipping prior injection."
        )
        return players_df

    prior_df = pd.read_csv(prior_stats_path)
    prior_df["norm_surname"] = prior_df["Surname"].apply(normalize_name)
    prior_df["norm_fullname"] = prior_df["FullName"].apply(normalize_name)

    matched_count = 0
    imputed_count = 0

    effective_tps = []
    form_factors = []

    for _, row in players_df.iterrows():
        surname = str(row["Surname"])
        norm_s = normalize_name(surname)
        pos = str(row["Position"])
        price = float(row.get("Price", 5.0))
        raw_current_tp = float(row.get("TP", 0.0))

        # Search match by normalized surname + position
        match = prior_df[
            (prior_df["norm_surname"] == norm_s) & (prior_df["Position"] == pos)
        ]
        if match.empty or len(match) > 1:
            fullname_match = prior_df[
                (prior_df["norm_fullname"].str.contains(norm_s, na=False))
                & (prior_df["Position"] == pos)
            ]
            if not fullname_match.empty:
                match = fullname_match

        if not match.empty:
            if len(match) > 1:
                # If initial prefix present in surname (e.g. B.Fernandes vs M.Fernandes)
                if "." in surname:
                    init = surname.split(".")[0].lower()
                    init_match = match[
                        match["FullName"].str.lower().str.startswith(init)
                    ]
                    if not init_match.empty:
                        match = init_match
                # Check team match
                team = str(row.get("Team", ""))
                team_match = match[match["Team"] == team]
                if not team_match.empty:
                    match = team_match
                # Price-tier tiebreaker
                if len(match) > 1:
                    if price >= 9.0:
                        match = match.sort_values(by="TotalPoints", ascending=False)
                    else:
                        match = match.sort_values(by="TotalPoints", ascending=True)

            prior_tp = float(match.iloc[0]["TotalPoints"])
            matched_count += 1
        else:
            # Impute based on Price * Position Benchmark
            ppm_benchmark = POSITION_PPM_BENCHMARKS.get(pos, 21.0)
            prior_tp = round(price * ppm_benchmark)
            imputed_count += 1

        # Synthesize Effective Total Points
        if current_gw <= 1:
            effective_tp = prior_tp
            form_factor = round(prior_tp * (2.0 / 38.0), 1)
        else:
            # Scale current in-season points to 38-game equivalent
            annualized_current_tp = raw_current_tp * (38.0 / (current_gw - 1))
            effective_tp = round(
                alpha_t * prior_tp + (1.0 - alpha_t) * annualized_current_tp
            )
            form_factor = raw_current_tp

        effective_tps.append(effective_tp)
        form_factors.append(form_factor)

    players_df["TP"] = effective_tps
    players_df["PPM"] = (players_df["TP"] / players_df["Price"]).round(2)
    players_df["Form_Factor"] = form_factors

    print(
        f"    - Prior baseline synthesized: {matched_count} historical matches, {imputed_count} imputed assets."
    )
    return players_df


def enrich_with_insight(gameweek_dir: str):
    """
    Loads the enriched database and injects our strategic insights, creating
    the final, prophetic dataset for the Chimera Prophet to consume.
    """
    print("--- [2/4] PROPHETIC ENRICHMENT PROTOCOL ONLINE ---")

    # --- Load Master Configuration ---
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        insight_config = config.get("enrich_insight", {})
        CAPTAINCY_TIERS = insight_config.get("captaincy_tiers", {})
        FORM_LOOKBACK = insight_config.get("form_lookback_weeks", 2)
        print("[+] Master configuration loaded.")
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(
            f"!!! WARNING: Could not load or parse config.yaml: {e}. "
            f"Using default fallbacks."
        )
        CAPTAINCY_TIERS = {
            "Gods": {
                "players": ["Haaland", "B.Fernandes", "Bruno Fernandes"],
                "coefficient": 1.20,
            },
            "Demigods": {
                "players": [
                    "Semenyo",
                    "João Pedro",
                    "Gabriel",
                    "Saka",
                    "Palmer",
                    "Thiago",
                ],
                "coefficient": 1.08,
            },
        }
        FORM_LOOKBACK = 2

    # --- Configuration ---
    SOURCE_DB_PATH = f"{gameweek_dir}/fpl_master_database_enriched.csv"
    PROPHETIC_DB_PATH = f"{gameweek_dir}/fpl_master_database_prophetic.csv"

    if not os.path.exists(SOURCE_DB_PATH):
        print(
            f"!!! CRITICAL FAILURE: Enriched database not found at "
            f"'{SOURCE_DB_PATH}'. Aborting."
        )
        return False

    try:
        players = pd.read_csv(SOURCE_DB_PATH)
        print(
            f"[+] Intelligence loaded. Preparing to imbue {len(players)} players "
            f"with strategic insight."
        )
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not read the database. Error: {e}")
        return False

    # Extract gameweek number
    current_gw_match = re.search(r"\d+", gameweek_dir)
    current_gw = int(current_gw_match.group()) if current_gw_match else 1

    # === BAYESIAN PRIOR & FORM SYNTHESIS ===
    players = inject_bayesian_prior_baseline(players, current_gw)

    # If GW >= 6, calculate rolling Form Factor from past GWs
    if current_gw >= 6:
        past_gw = current_gw - FORM_LOOKBACK
        if past_gw > 0:
            past_db_path = f"gw{past_gw}/fpl_master_database_enriched.csv"
            if os.path.exists(past_db_path):
                df_past = pd.read_csv(past_db_path)
                players = pd.merge(
                    players,
                    df_past[["Surname", "Team", "TP"]],
                    on=["Surname", "Team"],
                    how="left",
                    suffixes=("", "_past"),
                )
                players["TP_past"] = players["TP_past"].fillna(0)
                players["Form_Factor"] = players["TP"] - players["TP_past"]
                players.drop(columns=["TP_past"], inplace=True)
                print(
                    f"    - Form Factor calculated based on performance "
                    f"since GW{past_gw}."
                )
            else:
                players["Form_Factor"] = players["TP"]
        else:
            players["Form_Factor"] = players["TP"]

    # 1. Initialize all players as Mortals (Coef 1.0)
    players["Captaincy_Coef"] = 1.0
    print("[+] All players initialized as Mortals (Coef 1.0).")

    # 2. Anoint the Gods and Demigods
    if CAPTAINCY_TIERS:
        for tier_name, tier_data in CAPTAINCY_TIERS.items():
            player_list = tier_data.get("players", [])
            coef = tier_data.get("coefficient", 1.0)

            tier_mask = pd.Series(False, index=players.index)
            for p in player_list:
                if p == "Palmer":
                    # Disambiguate Cole Palmer (MID) from GKP Palmer
                    tier_mask = tier_mask | (
                        (players["Surname"] == "Palmer")
                        & (players["Position"] == "MID")
                    )
                elif p in ["B.Fernandes", "Bruno Fernandes"]:
                    tier_mask = tier_mask | (
                        players["Surname"].isin(["B.Fernandes", "Bruno Fernandes"])
                    )
                    tier_mask = tier_mask | (
                        (players["Surname"] == "Fernandes")
                        & (players["Team"] == "Man Utd")
                    )
                else:
                    tier_mask = (
                        tier_mask
                        | (players["Surname"] == p)
                        | (players["Surname"].str.contains(p, na=False))
                    )

            tier_indices = players[tier_mask].index
            players.loc[tier_indices, "Captaincy_Coef"] = coef
            print(
                f"    - Anointing {len(tier_indices)} players as {tier_name} (Coef {coef})."
            )
    else:
        print(
            "    - WARNING: No Captaincy Tiers defined in config. Skipping anointment."
        )

    # 3. Forge the Prophetic Points (PP)
    players["PP"] = (players["TP"] * players["Captaincy_Coef"]).round(2)
    print("[+] 'Prophetic_Points' (PP) metric forged. True value is now visible.")

    # 4. Verification: Show the results for our anointed heroes
    print("\n--- VERIFICATION: THE CHOSEN ONES ---")
    if CAPTAINCY_TIERS:
        anointed_surnames = [
            p
            for t in CAPTAINCY_TIERS.values()
            for p in cast(Dict[str, Any], t).get("players", [])
        ]
        verification_df = players[players["Surname"].isin(anointed_surnames)]
        if not verification_df.empty:
            cols_to_show = [
                "Surname",
                "Team",
                "TP",
                "Form_Factor",
                "Captaincy_Coef",
                "PP",
            ]
            # Cast to DataFrame to help type checkers resolve to_string
            subset_df = cast(pd.DataFrame, verification_df[cols_to_show])
            print(subset_df.to_string(index=False))
        else:
            print("No anointed players found to verify.")
    else:
        print("No Captaincy Tiers to verify.")

    # 5. Save the Prophetic Database
    try:
        players.to_csv(PROPHETIC_DB_PATH, index=False)
        print(
            f"\n--- SUCCESS: The Prophetic Database has been forged "
            f"at '{PROPHETIC_DB_PATH}' ---"
        )
        return True
    except Exception as e:
        print(
            f"!!! CRITICAL FAILURE: Could not save the prophetic database. Error: {e}"
        )
        return False


# --- Main Execution Block ---

# This block now only runs if you execute "python enrich_with_insight.py gw5" directly.
# It allows the script to still be used as a standalone tool.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python enrich_with_insight.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    enrich_with_insight(gameweek_directory)

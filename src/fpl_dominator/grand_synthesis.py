import os
import sys
from typing import List, cast

import numpy as np
import pandas as pd
import yaml

TEAM_NAME_TO_TLA = {
    "Arsenal": "ARS",
    "Aston Villa": "AVL",
    "Bournemouth": "BOU",
    "Brentford": "BRE",
    "Brighton": "BHA",
    "Chelsea": "CHE",
    "Coventry City": "COV",
    "Crystal Palace": "CRY",
    "Everton": "EVE",
    "Fulham": "FUL",
    "Hull City": "HUL",
    "Ipswich Town": "IPS",
    "Leeds": "LEE",
    "Liverpool": "LIV",
    "Man City": "MCI",
    "Man Utd": "MUN",
    "Newcastle": "NEW",
    "Nott'm Forest": "NFO",
    "Spurs": "TOT",
    "Sunderland": "SUN",
}


def synthesize_omniscient_data(
    players_df: pd.DataFrame,
    fixtures_df: pd.DataFrame,
    fixture_weights: List[float],
) -> pd.DataFrame:
    """Merges prophetic player database with temporally weighted fixture FDR.

    Pure function operating entirely in memory.

    Args:
        players_df: Prophetic player DataFrame with 'Team', 'Position', 'PP', etc.
        fixtures_df: Fixture difficulty DataFrame with 'Team', 'Gameweek',
            'FDR_A', 'FDR_D'.
        fixture_weights: Array of temporal weights for discounting future fixtures.

    Returns:
        Omniscient DataFrame containing Effective_FDR_Horizon_5GW and Projected_Score.

    Raises:
        ValueError: If unmapped team names are encountered.
    """
    p_df = players_df.copy()
    f_df = fixtures_df.copy()

    # 1. Prepare player team acronyms
    p_df["Team_TLA"] = p_df["Team"].replace(TEAM_NAME_TO_TLA)

    # Check for unmapped teams
    mask = p_df["Team_TLA"].isnull()
    if bool(mask.any()):
        unmapped_teams = list(set(p_df[mask]["Team"].tolist()))
        raise ValueError(
            f"Could not map the following team names to an acronym: {unmapped_teams}"
        )

    # 2. Sort fixtures chronologically before applying weights
    f_df["GW_Num"] = f_df["Gameweek"].str.extract(r"(\d+)").astype(int)
    f_df = f_df.sort_values(by=["Team", "GW_Num"])

    def weighted_fdr(series: pd.Series) -> float:
        weights_slice = fixture_weights[: len(series)]
        return float(np.average(series, weights=weights_slice))

    fdr_horizon = (
        f_df.groupby("Team")
        .agg(
            FDR_A_Horizon_5GW=("FDR_A", weighted_fdr),
            FDR_D_Horizon_5GW=("FDR_D", weighted_fdr),
        )
        .reset_index()
    )
    fdr_horizon = fdr_horizon.rename(columns={"Team": "Team_TLA"})

    # 3. Merge prophetic and temporal realities
    omniscient_df = pd.merge(p_df, fdr_horizon, on="Team_TLA", how="left")

    # 4. Positional bifurcation
    omniscient_df["Effective_FDR_Horizon_5GW"] = np.where(
        omniscient_df["Position"].isin(["GKP", "DEF"]),
        omniscient_df["FDR_D_Horizon_5GW"],
        omniscient_df["FDR_A_Horizon_5GW"],
    )

    # 5. Forge Projected Score
    omniscient_df["Projected_Score"] = (
        omniscient_df["PP"] / omniscient_df["Effective_FDR_Horizon_5GW"]
    ).round(2)

    return omniscient_df


def perform_grand_synthesis(
    gameweek_dir: str, fixture_weights: list[float] | None = None
) -> bool:
    """Merges Prophetic and Temporal realities and persists the Omniscient DB.

    Maintains full backwards compatibility with commander and CLI gauntlet.
    """
    print("--- [3/4] GRAND SYNTHESIS PROTOCOL ONLINE ---")

    # --- Load Master Configuration ---
    if fixture_weights is not None:
        if len(fixture_weights) != 5:
            print(
                f"!!! WARNING: 'fixture_weights' should have 5 values. "
                f"Found {len(fixture_weights)}. Using equal weights."
            )
            weights = [1.0, 1.0, 1.0, 1.0, 1.0]
        else:
            weights = fixture_weights
        print(f"[+] Custom fixture weights provided: {weights}")
    else:
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)

            temporal_config = config.get("temporal_discounting", {})
            weights = temporal_config.get("fixture_weights", [1.0, 1.0, 1.0, 1.0, 1.0])
            print("[+] Master configuration for Temporal Discounting loaded.")
            if len(weights) != 5:
                print(
                    f"!!! WARNING: 'fixture_weights' in config should have 5 values. "
                    f"Found {len(weights)}. Using equal weights."
                )
                weights = [1.0, 1.0, 1.0, 1.0, 1.0]

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(
                f"!!! WARNING: Could not load or parse config.yaml: {e}. "
                f"Using default fallbacks (equal weights)."
            )
            weights = [1.0, 1.0, 1.0, 1.0, 1.0]

    # --- File Paths ---
    prophetic_db_path = f"{gameweek_dir}/fpl_master_database_prophetic.csv"
    fixture_db_path = f"{gameweek_dir}/fixtures.csv"
    omniscient_db_path = f"{gameweek_dir}/fpl_master_database_OMNISCIENT.csv"

    # 1. Load Artifacts
    if not all(os.path.exists(p) for p in [prophetic_db_path, fixture_db_path]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return False

    players_df = pd.read_csv(prophetic_db_path)
    fixtures_df = pd.read_csv(fixture_db_path)
    print("[+] Both Prophetic and Fixture databases have been loaded.")

    try:
        omniscient_df = synthesize_omniscient_data(players_df, fixtures_df, weights)
    except ValueError as e:
        print(f"!!! CRITICAL FAILURE: {e}")
        return False

    print("[+] Prophetic and Temporal realities have been merged.")
    print("[+] 'Effective_FDR_Horizon_5GW' forged using positional bifurcation logic.")
    print("[+] Ultimate metric 'Projected_Score' has been forged using effective FDR.")

    # 2. Verification / Top prospects display
    print("\n--- TOP 15 PROSPECTS (BY PROJECTED SCORE OVER NEXT 5GW) ---")
    top_prospects = omniscient_df.sort_values(
        by="Projected_Score", ascending=False
    ).head(15)
    cols_to_show = [
        "Surname",
        "Team",
        "PP",
        "Effective_FDR_Horizon_5GW",
        "Projected_Score",
    ]
    subset_df = cast(pd.DataFrame, top_prospects[cols_to_show])
    print(subset_df.to_string(index=False))

    # 3. Save the Omniscient Database
    try:
        omniscient_df.to_csv(omniscient_db_path, index=False)
        print(
            f"\n--- SUCCESS: THE OMNISCIENT Database has been forged "
            f"at '{omniscient_db_path}' ---"
        )
        return True
    except Exception as e:
        print(
            f"!!! CRITICAL FAILURE: Could not save the omniscient database. Error: {e}"
        )
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python grand_synthesis.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    perform_grand_synthesis(gameweek_directory)

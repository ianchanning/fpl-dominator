import os
import sys
import yaml
import numpy as np
import pandas as pd


def perform_grand_synthesis(gameweek_dir: str):
    """
    Merges the Prophetic player database with the Temporal fixture database,
    creating the ultimate Omniscient dataset for our final Chimera.
    """
    print("--- [3/4] GRAND SYNTHESIS PROTOCOL ONLINE ---")

    # --- Load Master Configuration ---
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        temporal_config = config.get("temporal_discounting", {})
        FIXTURE_WEIGHTS = temporal_config.get(
            "fixture_weights", [1.0, 1.0, 1.0, 1.0, 1.0]
        )  # Fallback to mean
        print("[+] Master configuration for Temporal Discounting loaded.")
        if len(FIXTURE_WEIGHTS) != 5:
            print(
                f"!!! WARNING: 'fixture_weights' in config should have 5 values. Found {len(FIXTURE_WEIGHTS)}. Using equal weights."
            )
            FIXTURE_WEIGHTS = [1.0, 1.0, 1.0, 1.0, 1.0]

    except (FileNotFoundError, yaml.YAMLError) as e:
        print(
            f"!!! WARNING: Could not load or parse config.yaml: {e}. Using default fallbacks (equal weights)."
        )
        FIXTURE_WEIGHTS = [1.0, 1.0, 1.0, 1.0, 1.0]

    # --- File Paths & Mappings ---
    PROPHETIC_DB_PATH = f"{gameweek_dir}/fpl_master_database_prophetic.csv"
    FIXTURE_DB_PATH = f"{gameweek_dir}/fixtures.csv"
    OMNISCIENT_DB_PATH = f"{gameweek_dir}/fpl_master_database_OMNISCIENT.csv"
    TEAM_NAME_TO_TLA = {
        "Arsenal": "ARS",
        "Aston Villa": "AVL",
        "Brighton": "BHA",
        "Bournemouth": "BOU",
        "Brentford": "BRE",
        "Burnley": "BUR",
        "Chelsea": "CHE",
        "Crystal Palace": "CRY",
        "Everton": "EVE",
        "Fulham": "FUL",
        "Leeds": "LEE",
        "Liverpool": "LIV",
        "Man City": "MCI",
        "Man Utd": "MUN",
        "Newcastle": "NEW",
        "Nott'm Forest": "NFO",
        "Sunderland": "SUN",
        "Spurs": "TOT",
        "West Ham": "WHU",
        "Wolves": "WOL",
    }

    # 1. Load the Sacred Artifacts
    if not all(os.path.exists(p) for p in [PROPHETIC_DB_PATH, FIXTURE_DB_PATH]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return False

    players_df = pd.read_csv(PROPHETIC_DB_PATH)
    fixtures_df = pd.read_csv(FIXTURE_DB_PATH)
    print("[+] Both Prophetic and Fixture databases have been loaded.")

    # 2. Prepare the Player Data
    players_df["Team_TLA"] = players_df["Team"].map(TEAM_NAME_TO_TLA)
    if players_df["Team_TLA"].isnull().any():
        print("!!! WARNING: Some team names could not be mapped to an acronym.")
    print("[+] Player data prepared for temporal merging.")

    # 3. Evolve the FDR Horizon Calculation (Temporal Lens)

    # CRITICAL FIX: Ensure fixtures are sorted chronologically before applying weights.
    fixtures_df["GW_Num"] = fixtures_df["Gameweek"].str.extract(r"(\d+)").astype(int)
    fixtures_df.sort_values(by=["Team", "GW_Num"], inplace=True)
    print(
        "[+] Fixture data sorted chronologically to ensure correct temporal weighting."
    )

    def weighted_fdr(series):
        return np.average(series, weights=FIXTURE_WEIGHTS[: len(series)])

    print("[+] Calculating Temporally-Weighted FDR Horizons...")
    fdr_horizon = (
        fixtures_df.groupby("Team")
        .agg(
            FDR_A_Horizon_5GW=("FDR_A", weighted_fdr),
            FDR_D_Horizon_5GW=("FDR_D", weighted_fdr),
        )
        .reset_index()
    )
    fdr_horizon.rename(columns={"Team": "Team_TLA"}, inplace=True)
    print("[+] Trinity FDR Horizons (Attack/Defence) calculated using Temporal Lens.")

    # 4. The Grand Synthesis (The Merge)
    omniscient_df = pd.merge(players_df, fdr_horizon, on="Team_TLA", how="left")
    print("[+] Prophetic and Temporal realities have been merged.")

    # 5. Positional Bifurcation
    omniscient_df["Effective_FDR_Horizon_5GW"] = np.where(
        omniscient_df["Position"].isin(["GKP", "DEF"]),
        omniscient_df["FDR_D_Horizon_5GW"],
        omniscient_df["FDR_A_Horizon_5GW"],
    )
    print("[+] 'Effective_FDR_Horizon_5GW' forged using positional bifurcation logic.")

    # 6. Forge the Ultimate Metric: Projected Score
    omniscient_df["Projected_Score"] = (
        omniscient_df["PP"] / omniscient_df["Effective_FDR_Horizon_5GW"]
    ).round(2)
    print("[+] Ultimate metric 'Projected_Score' has been forged using effective FDR.")

    # 7. Verification
    print("\n--- TOP 15 PROSPECTS (BY PROJECTED SCORE OVER NEXT 5GW) ---")
    print(
        omniscient_df.sort_values(by="Projected_Score", ascending=False)
        .head(15)[
            ["Surname", "Team", "PP", "Effective_FDR_Horizon_5GW", "Projected_Score"]
        ]
        .to_string(index=False)
    )

    # 8. Save the Omniscient Database
    try:
        omniscient_df.to_csv(OMNISCIENT_DB_PATH, index=False)
        print(
            f"\n--- SUCCESS: The OMNISCIENT Database has been forged at '{OMNISCIENT_DB_PATH}' ---"
        )
        return True
    except Exception as e:
        print(
            f"!!! CRITICAL FAILURE: Could not save the omniscient database. Error: {e}"
        )
        return False


# --- Main Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python grand_synthesis.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    perform_grand_synthesis(gameweek_directory)

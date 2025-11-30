import pandas as pd
import numpy as np
import yaml

def verify_temporal_logic():
    """
    Runs a synthetic test case to verify that the temporal discounting
    logic for fixture difficulty is working as intended.
    """
    print("--- VERIFICATION PROTOCOL: TEMPORAL LENS ---")

    # --- Load Weights from Config ---
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        temporal_config = config.get("temporal_discounting", {})
        FIXTURE_WEIGHTS = temporal_config.get("fixture_weights", [1.0, 0.8, 0.6, 0.4, 0.2])
        print(f"[+] Using fixture weights from config: {FIXTURE_WEIGHTS}")
    except Exception as e:
        print(f"!!! WARNING: Could not load config, using default weights. Error: {e}")
        FIXTURE_WEIGHTS = [1.0, 0.8, 0.6, 0.4, 0.2]

    # --- Create Synthetic Data ---
    # Two teams with the same fixtures, but in a different order.
    # Team A: Hardest game first.
    # Team B: Hardest game last.
    data = {
        'Team': [
            'Team A', 'Team A', 'Team A', 'Team A', 'Team A',
            'Team B', 'Team B', 'Team B', 'Team B', 'Team B'
        ],
        'Gameweek': [
            'GW1', 'GW2', 'GW3', 'GW4', 'GW5',
            'GW1', 'GW2', 'GW3', 'GW4', 'GW5'
        ],
        'FDR': [
            1400, 1000, 1000, 1000, 1000,  # Team A
            1000, 1000, 1000, 1000, 1400   # Team B
        ]
    }
    fixtures_df = pd.DataFrame(data)
    fixtures_df['GW_Num'] = fixtures_df['Gameweek'].str.extract(r'(\d+)').astype(int)
    fixtures_df.sort_values(by=['Team', 'GW_Num'], inplace=True)
    
    print("\n[+] Synthetic Fixture Data:")
    print(fixtures_df[['Team', 'Gameweek', 'FDR']].to_string(index=False))

    # --- Run Calculations ---
    
    # 1. Simple Mean (the old way)
    mean_fdr = fixtures_df.groupby('Team').agg(Mean_FDR=('FDR', 'mean')).reset_index()

    # 2. Weighted Average (the new, correct way)
    def weighted_fdr(series):
        return np.average(series, weights=FIXTURE_WEIGHTS[:len(series)])

    weighted_fdr_horizon = fixtures_df.groupby('Team').agg(Weighted_FDR=('FDR', weighted_fdr)).reset_index()

    # --- Display Results ---
    print("\n--- RESULTS ---")
    print("\n[1] Simple Mean FDR (Old Logic):")
    print(mean_fdr.to_string(index=False))
    print("\nObservation: The teams are ranked identically, as the average difficulty is the same.")

    print("\n[2] Temporally-Weighted FDR (New Logic):")
    print(weighted_fdr_horizon.to_string(index=False))
    print("\nObservation: Team A, with the hard fixture first, is now correctly rated as having a more difficult immediate horizon.")
    
    print("\n--- VERDICT ---")
    if weighted_fdr_horizon.iloc[0]['Weighted_FDR'] > weighted_fdr_horizon.iloc[1]['Weighted_FDR']:
        print("✅ SUCCESS: The Temporal Lens is working correctly. The logic properly discounts future fixtures.")
    else:
        print("❌ FAILURE: The Temporal Lens is NOT working as expected.")


if __name__ == "__main__":
    verify_temporal_logic()

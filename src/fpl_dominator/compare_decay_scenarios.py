"""Compares Starting XI selections across multiple temporal decay scenarios.

Runs the Chimera solver against three decay profiles:
1. Eternalist (Flat): [1.0, 1.0, 1.0, 1.0, 1.0]
2. Balanced (Moderate Exponential 0.6): [1.0, 0.6, 0.36, 0.22, 0.13]
3. Sniper (Aggressive Exponential 0.2): [1.0, 0.2, 0.04, 0.01, 0.00]

Identifies locked Immortals (Robustness = 1.0), Horizon-Dependents, and Pure Punts.
"""

import sys
from typing import Dict, List, Set, Tuple

import pandas as pd

from .chimera_pyomo_v2 import forge_pyomo_squad
from .grand_synthesis import perform_grand_synthesis
from .temporal_decay import generate_exponential_weights


def classify_player(
    in_flat: bool, in_moderate: bool, in_sniper: bool
) -> Tuple[str, float]:
    """Classifies player based on their selection across the 3 decay horizons."""
    selections = sum([in_flat, in_moderate, in_sniper])
    robustness = round(selections / 3.0, 2)

    if selections == 3:
        return "IMMORTAL", robustness
    if in_flat and in_moderate and not in_sniper:
        return "HORIZON-DEPENDENT", robustness
    if not in_flat and not in_moderate and in_sniper:
        return "PURE PUNT", robustness
    if not in_flat and in_moderate and in_sniper:
        return "RECENCY-SURGE", robustness
    if in_flat and not in_moderate and not in_sniper:
        return "LONG-RANGE BIAS", robustness
    return "ROTATIONAL", robustness


def run_decay_comparison(gameweek_dir: str) -> pd.DataFrame:
    """Executes 3 solves with varying temporal decay and returns comparison table."""
    title = f"RUNNING TEMPORAL DECAY COMPARISON ({gameweek_dir.upper()})"
    print(f"\n{'=' * 20} {title} {'=' * 20}")

    profiles: Dict[str, List[float]] = {
        "Flat (1.0)": [1.0, 1.0, 1.0, 1.0, 1.0],
        "Moderate (0.6)": generate_exponential_weights(0.6),
        "Sniper (0.2)": generate_exponential_weights(0.2),
    }

    starters_by_profile: Dict[str, pd.DataFrame] = {}
    player_info: Dict[str, Dict[str, object]] = {}

    for profile_name, weights in profiles.items():
        print(f"\n>>> [PROFILE: {profile_name}] Weight Horizon: {weights}")
        synthesis_ok = perform_grand_synthesis(gameweek_dir, fixture_weights=weights)
        if not synthesis_ok:
            raise RuntimeError(f"Grand synthesis failed for profile {profile_name}")

        solver_ok, starters, _ = forge_pyomo_squad(
            gameweek_dir, return_squad=True, force_reforge=True
        )
        if not solver_ok:
            raise RuntimeError(f"Pyomo solver failed for profile {profile_name}")

        starters_by_profile[profile_name] = starters
        for _, row in starters.iterrows():
            surname = str(row["Surname"])
            if surname not in player_info:
                player_info[surname] = {
                    "Surname": surname,
                    "Team": row["Team"],
                    "Position": row["Position"],
                    "Price": row["Price"],
                }

    # Collate comparison matrix
    records = []
    flat_set: Set[str] = set(starters_by_profile["Flat (1.0)"]["Surname"])
    mod_set: Set[str] = set(starters_by_profile["Moderate (0.6)"]["Surname"])
    sniper_set: Set[str] = set(starters_by_profile["Sniper (0.2)"]["Surname"])

    all_starters = set(flat_set | mod_set | sniper_set)

    for surname in all_starters:
        info = player_info[surname]
        in_flat = surname in flat_set
        in_mod = surname in mod_set
        in_sniper = surname in sniper_set

        classification, robustness = classify_player(in_flat, in_mod, in_sniper)

        records.append(
            {
                "Surname": surname,
                "Position": info["Position"],
                "Team": info["Team"],
                "Price": info["Price"],
                "Flat (1.0)": "✓" if in_flat else ".",
                "Mod (0.6)": "✓" if in_mod else ".",
                "Sniper (0.2)": "✓" if in_sniper else ".",
                "Robustness": f"{int(robustness * 100)}%",
                "Classification": classification,
            }
        )

    comparison_df = pd.DataFrame(records)

    # Positional ordering
    pos_order = {"GKP": 0, "DEF": 1, "MID": 2, "FWD": 3}
    comparison_df["pos_rank"] = comparison_df["Position"].map(pos_order)
    comparison_df.sort_values(
        by=["pos_rank", "Robustness", "Price"],
        ascending=[True, False, False],
        inplace=True,
    )
    comparison_df.drop(columns=["pos_rank"], inplace=True)

    # Print output table
    print("\n" + "=" * 30 + " STABILITY MATRIX " + "=" * 30)
    print(comparison_df.to_string(index=False))

    immortals = comparison_df[comparison_df["Classification"] == "IMMORTAL"][
        "Surname"
    ].tolist()
    print("\n" + "-" * 78)
    print(f"[*] THE IMMORTALS ({len(immortals)} Locks): {', '.join(immortals)}")
    print("-" * 78)

    # Restore default master database from config.yaml
    print("\n[+] Restoring baseline config.yaml state...")
    perform_grand_synthesis(gameweek_dir)
    forge_pyomo_squad(gameweek_dir, force_reforge=True)
    print("[+] Baseline state fully restored.")

    return comparison_df


if __name__ == "__main__":
    gw_dir = sys.argv[1] if len(sys.argv) > 1 else "gw3"
    run_decay_comparison(gw_dir)

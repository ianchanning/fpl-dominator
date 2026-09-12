import os
from typing import Dict, Tuple

import pandas as pd

from fpl_dominator.grand_synthesis import TEAM_NAME_TO_TLA

# Baseline expected points per 90 / match by position for parity FDR (1150.0)
POSITIONAL_BASELINE_EXP_POINTS: Dict[str, float] = {
    "GKP": 3.5,
    "DEF": 3.5,
    "MID": 4.5,
    "FWD": 4.5,
}
PARITY_FDR: float = 1150.0
FDR_NORMALIZATION_SCALAR: float = 1000.0


def extract_historical_fixture_fdr(
    current_gw: int, lookback_weeks: int = 2
) -> Dict[Tuple[str, int], Dict[str, float]]:
    """Extracts historical FDR metrics for teams across lookback gameweeks.

    Searches past gameweek vaults (`gw{g}/fixtures.csv`) for fixture difficulties
    encountered during gameweeks g in [current_gw - lookback_weeks, current_gw - 1].

    Args:
        current_gw: The gameweek being processed (e.g. 4).
        lookback_weeks: Number of preceding gameweeks in lookback window.

    Returns:
        Dictionary mapping (team_tla, gameweek_num) to FDR dictionary:
        {"FDR": float, "FDR_A": float, "FDR_D": float}.
    """
    fdr_map: Dict[Tuple[str, int], Dict[str, float]] = {}
    start_gw = max(1, current_gw - lookback_weeks)
    target_gws = list(range(start_gw, current_gw))

    for gw in target_gws:
        gw_label = f"GW{gw}"
        # Primary source: gw{gw}/fixtures.csv, fallback to gw{current_gw}
        fixture_candidates = [
            f"gw{gw}/fixtures.csv",
            f"gw{current_gw}/fixtures.csv",
        ]
        for candidate in fixture_candidates:
            if not os.path.exists(candidate):
                continue
            try:
                fix_df = pd.read_csv(candidate)
                if "Gameweek" not in fix_df.columns or "Team" not in fix_df.columns:
                    continue
                gw_matches = fix_df[fix_df["Gameweek"] == gw_label]
                if gw_matches.empty:
                    continue

                for _, row in gw_matches.iterrows():
                    team_tla = str(row["Team"]).strip().upper()
                    fdr = float(row.get("FDR", PARITY_FDR))
                    fdr_a = float(row.get("FDR_A", fdr))
                    fdr_d = float(row.get("FDR_D", fdr))

                    key = (team_tla, gw)
                    if key not in fdr_map:
                        fdr_map[key] = {
                            "FDR": fdr,
                            "FDR_A": fdr_a,
                            "FDR_D": fdr_d,
                        }
                if any(k[1] == gw for k in fdr_map):
                    break  # Found fixtures for this gameweek
            except Exception as e:
                print(f"    - [!] Warning reading fixtures from {candidate}: {e}")

    return fdr_map


def extract_historical_player_points(
    current_gw: int, lookback_weeks: int = 2
) -> Dict[Tuple[str, str], Dict[int, float]]:
    """Extracts points scored by each player in each historical gameweek.

    Calculates per-gameweek delta points: Points_g = TP_g - TP_{g-1} by loading
    `fpl_master_database_enriched.csv` from respective historical vaults.

    Args:
        current_gw: The current gameweek number being prepared.
        lookback_weeks: Number of weeks in the lookback window.

    Returns:
        Dictionary mapping (surname, team) -> {gameweek_num: delta_points}.
    """
    start_gw = max(1, current_gw - lookback_weeks)
    # Need start_gw - 1 for diff baseline
    needed_gws = list(range(start_gw - 1, current_gw))

    tp_snapshots: Dict[int, Dict[Tuple[str, str], float]] = {}

    for gw in needed_gws:
        if gw == 0:
            # Baseline before GW1 is 0 points for all players
            tp_snapshots[0] = {}
            continue

        vault_db = f"gw{gw}/fpl_master_database_enriched.csv"
        if not os.path.exists(vault_db):
            continue

        try:
            df = pd.read_csv(vault_db)
            if "Surname" not in df.columns or "TP" not in df.columns:
                continue

            snapshot: Dict[Tuple[str, str], float] = {}
            for _, row in df.iterrows():
                surname = str(row["Surname"]).strip()
                team = str(row.get("Team", "")).strip()
                tp = float(row.get("TP", 0.0))
                snapshot[(surname, team)] = tp
            tp_snapshots[gw] = snapshot
        except Exception as e:
            print(f"    - [!] Warning reading historical DB {vault_db}: {e}")

    # Compute per-gameweek deltas
    delta_map: Dict[Tuple[str, str], Dict[int, float]] = {}
    target_gws = list(range(start_gw, current_gw))

    for gw in target_gws:
        curr_snap = tp_snapshots.get(gw, {})
        prev_snap = tp_snapshots.get(gw - 1, {})

        for player_key, curr_tp in curr_snap.items():
            if player_key not in delta_map:
                delta_map[player_key] = {}

            if gw - 1 == 0:
                # Delta for GW1 is just points in GW1
                delta = curr_tp
            elif player_key in prev_snap:
                delta = max(0.0, curr_tp - prev_snap[player_key])
            else:
                # New transfer not in previous snapshot; use full current TP
                delta = curr_tp

            delta_map[player_key][gw] = delta

    return delta_map


def calculate_retrospective_form(
    players_df: pd.DataFrame,
    current_gw: int,
    lookback_weeks: int = 2,
) -> pd.DataFrame:
    """Calculates Fixture-Adjusted Form and Form Efficiency for all players.

    Conforms to RFC-011 specifications:
    1. Adjusted_Form = Sum_{g} (Points_g * (FDR_past_g / 1000.0))
       - Evaluates against FDR_A for MID/FWD and FDR_D for GKP/DEF.
    2. Form_Efficiency = Sum(Points_g) / Sum(Expected_Points(FDR_past_g))

    Args:
        players_df: DataFrame containing player data (Surname, Team, Position, etc.).
        current_gw: Target gameweek number being prepared.
        lookback_weeks: Lookback depth in gameweeks (default 2).

    Returns:
        Updated DataFrame with 'Raw_Form', 'Adjusted_Form', and 'Form_Efficiency'.
    """
    df = players_df.copy()

    # Extract historical FDRs and points deltas
    fdr_map = extract_historical_fixture_fdr(current_gw, lookback_weeks)
    points_delta_map = extract_historical_player_points(current_gw, lookback_weeks)

    start_gw = max(1, current_gw - lookback_weeks)
    target_gws = list(range(start_gw, current_gw))

    raw_forms: list[float] = []
    adjusted_forms: list[float] = []
    form_efficiencies: list[float] = []

    for _, row in df.iterrows():
        surname = str(row["Surname"]).strip()
        team = str(row.get("Team", "")).strip()
        pos = str(row.get("Position", "MID")).strip().upper()
        team_tla = TEAM_NAME_TO_TLA.get(team, team[:3].upper())

        player_deltas = points_delta_map.get((surname, team), {})

        # Fallback if player not in historical snapshots (e.g. GW1 or new addition)
        if not player_deltas and target_gws:
            raw_tp = float(row.get("TP", 0.0))
            avg_per_gw = raw_tp / max(1, len(target_gws))
            player_deltas = {gw: avg_per_gw for gw in target_gws}

        total_raw_points = 0.0
        total_adjusted_points = 0.0
        total_expected_points = 0.0

        for gw in target_gws:
            gw_points = float(player_deltas.get(gw, 0.0))
            total_raw_points += gw_points

            # Retrieve FDR for this team and gameweek
            fix_fdr = fdr_map.get((team_tla, gw), {})
            if pos in ["GKP", "DEF"]:
                fdr_val = fix_fdr.get("FDR_D", fix_fdr.get("FDR", PARITY_FDR))
            else:
                fdr_val = fix_fdr.get("FDR_A", fix_fdr.get("FDR", PARITY_FDR))

            # Adjusted Form: Points * (FDR / 1000.0)
            fdr_multiplier = fdr_val / FDR_NORMALIZATION_SCALAR
            total_adjusted_points += gw_points * fdr_multiplier

            # Form Efficiency: Expected points based on difficulty
            base_exp = POSITIONAL_BASELINE_EXP_POINTS.get(pos, 4.0)
            exp_pts_gw = base_exp * (PARITY_FDR / max(800.0, fdr_val))
            total_expected_points += exp_pts_gw

        raw_form = round(total_raw_points, 2)
        adjusted_form = round(total_adjusted_points, 2)
        efficiency = (
            round(total_raw_points / max(0.5, total_expected_points), 2)
            if total_expected_points > 0.0
            else 1.0
        )

        raw_forms.append(raw_form)
        adjusted_forms.append(adjusted_form)
        form_efficiencies.append(efficiency)

    df["Raw_Form"] = raw_forms
    df["Adjusted_Form"] = adjusted_forms
    df["Form_Efficiency"] = form_efficiencies

    return df

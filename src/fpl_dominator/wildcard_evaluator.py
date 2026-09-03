"""
Wildcard Evaluator - Brutal Minimal Implementation (RFC-004)
Quantifies squad divergence, transition friction, and option value to
determine whether to trigger the Wildcard.
"""

import os
import re
from typing import Any, Dict, List

import pandas as pd
import pyomo.environ as pyo
import yaml

from .chimera_pyomo_v2 import (
    forge_pyomo_squad,
    sanitize_name,
)
from .enrich_with_insight import enrich_with_insight
from .forge_cauldron import forge_cauldron
from .grand_synthesis import perform_grand_synthesis


def calculate_squad_divergence(gameweek_dir: str) -> Dict[str, Any]:
    """
    Performs a brutal minimal evaluation comparing the current squad to the global optimal squad.
    Calculates:
      - Current Squad Projected Score (Starting XI)
      - Optimal Squad Projected Score (Starting XI)
      - Point Gap (Divergence Delta)
      - Transfer Distance (number of transfers required to reach optimal)
      - Path A (Status Quo - 0 hits), Path B (Manual Migration with hits),
        Path C (Wildcard Reset)
      - Recommendation based on RFC-004 dynamic option threshold
    """
    final_db_path = f"{gameweek_dir}/fpl_master_database_FINAL_v5.csv"
    squad_csv_path = f"{gameweek_dir}/squad.csv"

    if not os.path.exists(final_db_path):
        forge_cauldron(gameweek_dir)
        enrich_with_insight(gameweek_dir)
        perform_grand_synthesis(gameweek_dir)
        forge_pyomo_squad(gameweek_dir)

    if not os.path.exists(final_db_path):
        raise FileNotFoundError(f"Could not find or generate '{final_db_path}'")

    if not os.path.exists(squad_csv_path):
        raise FileNotFoundError(f"Squad file not found at '{squad_csv_path}'")

    master_df = pd.read_csv(final_db_path)
    current_squad_df = pd.read_csv(squad_csv_path)

    # Clean surname matching
    master_df["match_key"] = master_df["Surname"].apply(sanitize_name)
    current_squad_df["match_key"] = current_squad_df["Surname"].apply(sanitize_name)

    # Join current squad with master metrics
    joined_current = pd.merge(
        current_squad_df,
        master_df[
            [
                "match_key",
                "Team",
                "Position",
                "Final_Score",
                "Effective_FDR_Horizon_5GW",
                "Price",
            ]
        ],
        on=["match_key", "Position"],
        how="left",
        suffixes=("", "_master"),
    )

    joined_current["Final_Score"] = joined_current["Final_Score"].fillna(0.0)

    # Determine best starting XI for current squad (respecting FPL
    # formation rules: 1 GKP, >=3 DEF, >=1 FWD, exactly 11 players)
    gkps = joined_current[joined_current["Position"] == "GKP"].sort_values(
        by="Final_Score", ascending=False
    )
    defs = joined_current[joined_current["Position"] == "DEF"].sort_values(
        by="Final_Score", ascending=False
    )
    mids = joined_current[joined_current["Position"] == "MID"].sort_values(
        by="Final_Score", ascending=False
    )
    fwds = joined_current[joined_current["Position"] == "FWD"].sort_values(
        by="Final_Score", ascending=False
    )

    best_current_xi_score = -1.0
    best_current_xi_players: List[pd.Series] = []

    for d_count in [3, 4, 5]:
        for f_count in [1, 2, 3]:
            m_count = 10 - d_count - f_count
            if (
                2 <= m_count <= 5
                and len(defs) >= d_count
                and len(fwds) >= f_count
                and len(mids) >= m_count
                and len(gkps) >= 1
            ):
                selected = pd.concat(
                    [
                        gkps.iloc[:1],
                        defs.iloc[:d_count],
                        mids.iloc[:m_count],
                        fwds.iloc[:f_count],
                    ]
                )
                score = selected["Final_Score"].sum()
                if score > best_current_xi_score:
                    best_current_xi_score = score
                    best_current_xi_players = [row for _, row in selected.iterrows()]

    current_xi_df = pd.DataFrame(best_current_xi_players)

    # Run Pyomo to get unconstrained Global Optimum
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f).get("pyomo_solver", {})
    thrift_factor = config.get("thrift_factor", 0.001)
    bench_potency_epsilon = config.get("bench_potency_epsilon", 0.00001)

    model = pyo.ConcreteModel(name="Optimal_Wildcard_Squad")
    player_indices = master_df.index.tolist()
    model.players = pyo.Set(initialize=player_indices)

    final_scores = master_df["Final_Score"].to_dict()
    prices = master_df["Price"].to_dict()
    positions = master_df["Position"].to_dict()
    teams = master_df["Team_TLA"].to_dict()

    model.in_squad = pyo.Var(model.players, within=pyo.Binary)
    model.is_starter = pyo.Var(model.players, within=pyo.Binary)

    def objective_rule(m):
        starter_score = sum(final_scores[i] * m.is_starter[i] for i in m.players)
        bench_penalty = sum(
            (m.in_squad[i] - m.is_starter[i]) * prices[i] * thrift_factor
            for i in m.players
        )
        bench_bonus = sum(
            (m.in_squad[i] - m.is_starter[i]) * final_scores[i] * bench_potency_epsilon
            for i in m.players
        )
        return starter_score - bench_penalty + bench_bonus

    model.objective = pyo.Objective(rule=objective_rule, sense=pyo.maximize)

    current_team_value = (
        current_squad_df["SP"].astype(float).sum()
        if "SP" in current_squad_df.columns
        else 100.0
    )
    budget_limit = max(100.0, current_team_value)

    model.squad_cost = pyo.Constraint(
        expr=sum(prices[i] * model.in_squad[i] for i in model.players) <= budget_limit
    )
    model.squad_size = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players) == 15
    )
    model.gkp_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "GKP") == 2
    )
    model.def_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "DEF") == 5
    )
    model.mid_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "MID") == 5
    )
    model.fwd_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "FWD") == 3
    )

    model.team_list = pyo.Set(initialize=master_df["Team_TLA"].unique())

    def team_limit_rule(m, team_tla):
        return sum(m.in_squad[i] for i in m.players if teams[i] == team_tla) <= 3

    model.team_limit = pyo.Constraint(model.team_list, rule=team_limit_rule)

    model.starter_size = pyo.Constraint(
        expr=sum(model.is_starter[i] for i in model.players) == 11
    )
    model.starter_gkp = pyo.Constraint(
        expr=sum(model.is_starter[i] for i in model.players if positions[i] == "GKP")
        == 1
    )
    model.starter_def = pyo.Constraint(
        expr=sum(model.is_starter[i] for i in model.players if positions[i] == "DEF")
        >= 3
    )
    model.starter_fwd = pyo.Constraint(
        expr=sum(model.is_starter[i] for i in model.players if positions[i] == "FWD")
        >= 1
    )
    model.bridge = pyo.Constraint(
        model.players, rule=lambda m, i: m.is_starter[i] <= m.in_squad[i]
    )

    solver = pyo.SolverFactory("glpk")
    solver.solve(model, tee=False)

    opt_squad_indices = [i for i in model.players if pyo.value(model.in_squad[i]) == 1]
    opt_starter_indices = [
        i for i in model.players if pyo.value(model.is_starter[i]) == 1
    ]

    optimal_squad_df = master_df.loc[opt_squad_indices].copy()
    optimal_starters_df = master_df.loc[opt_starter_indices].copy()
    optimal_xi_score = optimal_starters_df["Final_Score"].sum()

    # Calculate Transfer Distance (symmetric difference between 15-man squads)
    current_match_keys = set(joined_current["match_key"].tolist())
    optimal_match_keys = set(optimal_squad_df["match_key"].tolist())

    players_to_keep = current_match_keys.intersection(optimal_match_keys)
    transfers_needed = 15 - len(players_to_keep)

    gw_match = re.search(r"\d+", gameweek_dir)
    current_gw = int(gw_match.group()) if gw_match else 2

    # Scale score to 5-week point units
    projected_pts_current_5gw = best_current_xi_score * 100.0
    projected_pts_optimal_5gw = optimal_xi_score * 100.0
    pts_divergence = projected_pts_optimal_5gw - projected_pts_current_5gw

    # Dynamic threshold: early season threshold is high
    # (option value of holding is high)
    threshold_pts = max(12.0, 32.0 - (current_gw - 2) * 1.3)

    # 3-Path Evaluation:
    path_a_pts = projected_pts_current_5gw + min(pts_divergence * 0.35, 12.0)
    hit_count = max(0, min(transfers_needed - 1, 4))
    path_b_pts = (projected_pts_current_5gw + pts_divergence * 0.75) - (hit_count * 4.0)
    path_c_pts = projected_pts_optimal_5gw

    wc_advantage = path_c_pts - max(path_a_pts, path_b_pts)
    should_trigger = wc_advantage >= threshold_pts

    return {
        "gameweek": current_gw,
        "current_xi_score": best_current_xi_score,
        "optimal_xi_score": optimal_xi_score,
        "projected_pts_current_5gw": projected_pts_current_5gw,
        "projected_pts_optimal_5gw": projected_pts_optimal_5gw,
        "pts_divergence": pts_divergence,
        "transfers_needed": transfers_needed,
        "players_to_keep": list(players_to_keep),
        "path_a_pts": path_a_pts,
        "path_b_pts": path_b_pts,
        "path_c_pts": path_c_pts,
        "wc_advantage": wc_advantage,
        "threshold_pts": threshold_pts,
        "should_trigger": should_trigger,
        "current_xi_df": current_xi_df,
        "optimal_starters_df": optimal_starters_df,
        "optimal_squad_df": optimal_squad_df,
    }

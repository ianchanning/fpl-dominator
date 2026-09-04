import os
import re
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import pandas as pd
import pyomo.environ as pyo
import yaml

TEAM_SHORT_TO_FULL = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Brighton": "Brighton and Hove Albion",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Coventry City": "Coventry City",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Hull City": "Hull City",
    "Ipswich Town": "Ipswich Town",
    "Leeds": "Leeds United",
    "Liverpool": "Liverpool",
    "Man City": "Manchester City",
    "Man Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Nott'm Forest": "Nottingham Forest",
    "Spurs": "Tottenham Hotspur",
    "Sunderland": "Sunderland",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
}

DEFAULT_SPP_SCORES = {
    "Penalties": {"primary": 5.0, "secondary": 2.5},
    "Direct Free Kicks": {"primary": 2.5, "secondary": 1.25},
    "Corners & Indirect Free Kicks": {"primary": 1.5, "secondary": 0.75},
}


@dataclass(frozen=True)
class SquadSolution:
    """Structured in-memory solution container for Chimera MILP solves."""

    success: bool
    starters: pd.DataFrame
    bench: pd.DataFrame
    squad: pd.DataFrame
    enriched_df: pd.DataFrame
    total_score: float
    total_cost: float
    bank: float


def sanitize_name(name: str) -> str:
    """Sanitizes player names for fuzzy set-piece matching."""
    return re.sub(r"[\.\-\s\(\)]", "", name.lower())


def enrich_with_set_pieces(
    players_df: pd.DataFrame,
    set_piece_path: str,
    score_model: Dict[str, Dict[str, float]],
) -> pd.DataFrame:
    """Enriches players with Set-Piece Potency (SPP) scores."""
    print("[+] Beginning Set-Piece Potency (SPP) enrichment...")
    df = players_df.copy()
    if not os.path.exists(set_piece_path):
        print(
            f"!!! WARNING: Set-piece database not found at '{set_piece_path}'. "
            f"Setting SPP to 0.0."
        )
        df["SPP"] = 0.0
        return df

    set_pieces_df = pd.read_csv(set_piece_path)
    df["SPP"] = 0.0
    df["match_key"] = df["Surname"].apply(sanitize_name)
    df["Team_Full_For_Join"] = df["Team"].map(TEAM_SHORT_TO_FULL).fillna(df["Team"])

    for _, row in set_pieces_df.iterrows():
        club_full_name = row["Club"]
        duties = {
            "Penalties": str(row["Penalties"]).split(","),
            "Direct Free Kicks": str(row["Direct Free Kicks"]).split(","),
            "Corners & Indirect Free Kicks": str(
                row["Corners & Indirect Free Kicks"]
            ).split(","),
        }

        for duty_type, takers in duties.items():
            if duty_type not in score_model:
                continue
            for i, taker_name in enumerate(takers):
                sanitized_taker = sanitize_name(taker_name.strip())
                target_indices = df[
                    (df["Team_Full_For_Join"] == club_full_name)
                    & (df["match_key"].str.contains(sanitized_taker, na=False))
                ].index

                if not target_indices.empty:
                    score = (
                        score_model[duty_type]["primary"]
                        if i == 0
                        else score_model[duty_type]["secondary"]
                    )
                    df.loc[target_indices, "SPP"] += score

    df.drop(columns=["match_key", "Team_Full_For_Join"], inplace=True)
    print("[+] SPP enrichment complete.")
    return df


def solve_chimera_squad(
    omniscient_df: pd.DataFrame,
    set_pieces_path: str = "set_pieces.csv",
    solver_config: Optional[Dict[str, object]] = None,
) -> SquadSolution:
    """Solves the Chimera MILP optimization entirely in memory.

    Decoupled from filesystem reads/writes to enable high-speed parallel or
    gradient scenario solves without race conditions or disk collisions.

    Args:
        omniscient_df: Omniscient DataFrame containing player intelligence.
        set_pieces_path: Path to set pieces database.
        solver_config: Optional dictionary of solver settings (from config.yaml).

    Returns:
        SquadSolution dataclass containing starters, bench, squad,
        and financial metrics.
    """
    if solver_config is None:
        try:
            with open("config.yaml", "r") as f:
                solver_config = yaml.safe_load(f).get("pyomo_solver", {}) or {}
        except (FileNotFoundError, yaml.YAMLError):
            solver_config = {}

    thrift_factor = float(solver_config.get("thrift_factor", 0.001))
    bench_potency_epsilon = float(solver_config.get("bench_potency_epsilon", 0.00001))
    form_factor_weight = float(solver_config.get("form_factor_weight", 0.7))
    red_zone_threshold = float(solver_config.get("red_zone_threshold", 1250))
    red_zone_limit = int(solver_config.get("red_zone_limit", 5))
    spp_scores = solver_config.get("spp_scores", DEFAULT_SPP_SCORES)

    # Prepare DataFrame and enrich
    df = omniscient_df.copy()
    if "SPP" not in df.columns:
        df = enrich_with_set_pieces(df, set_pieces_path, spp_scores)

    # Compute Final_Score
    df["Final_Score"] = (
        df["PP"] + df["SPP"] + (df["Form_Factor"] * form_factor_weight)
    ) / df["Effective_FDR_Horizon_5GW"]

    # --- 1. Pyomo Model Construction ---
    model = pyo.ConcreteModel(name="FPL_Pyomo_Chimera_V3_Trinity")
    player_indices = df.index.tolist()
    model.players = pyo.Set(initialize=player_indices)

    final_scores = df["Final_Score"].to_dict()
    prices = df["Price"].to_dict()
    positions = df["Position"].to_dict()
    teams = df["Team_TLA"].to_dict()
    fdr_values = df["Effective_FDR_Horizon_5GW"].to_dict()

    # --- 2. Decision Variables ---
    model.in_squad = pyo.Var(model.players, within=pyo.Binary)
    model.is_starter = pyo.Var(model.players, within=pyo.Binary)

    # --- 3. Objective Function ---
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

    # --- 4. Constraints ---
    model.squad_cost = pyo.Constraint(
        expr=sum(prices[i] * model.in_squad[i] for i in model.players) <= 100.0
    )
    model.squad_size = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players) == 15
    )

    model.gkp_squad_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "GKP") == 2
    )
    model.def_squad_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "DEF") == 5
    )
    model.mid_squad_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "MID") == 5
    )
    model.fwd_squad_limit = pyo.Constraint(
        expr=sum(model.in_squad[i] for i in model.players if positions[i] == "FWD") == 3
    )

    # Team Limits (Max 3 per club)
    model.team_list = pyo.Set(initialize=df["Team_TLA"].unique())

    def team_limit_rule(m, team_tla):
        return sum(m.in_squad[i] for i in m.players if teams[i] == team_tla) <= 3

    model.team_limit = pyo.Constraint(model.team_list, rule=team_limit_rule)

    # Starter Size and Formations
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

    # Bridge Constraint
    def bridge_rule(m, i):
        return m.is_starter[i] <= m.in_squad[i]

    model.bridge = pyo.Constraint(model.players, rule=bridge_rule)

    # Red Zone Constraint
    def red_zone_rule(m):
        red_zone_players = [
            i for i in m.players if fdr_values.get(i, 0) > red_zone_threshold
        ]
        if not red_zone_players:
            return pyo.Constraint.Feasible
        return sum(m.is_starter[i] for i in red_zone_players) <= red_zone_limit

    model.red_zone_limit = pyo.Constraint(rule=red_zone_rule)

    # --- 5. Solver Invocation ---
    solver = pyo.SolverFactory("glpk")
    result = solver.solve(model, tee=False)

    if result.solver.termination_condition != pyo.TerminationCondition.optimal:
        return SquadSolution(
            success=False,
            starters=pd.DataFrame(),
            bench=pd.DataFrame(),
            squad=pd.DataFrame(),
            enriched_df=df,
            total_score=0.0,
            total_cost=0.0,
            bank=0.0,
        )

    squad_indices = [i for i in model.players if pyo.value(model.in_squad[i]) == 1]
    starter_indices = [i for i in model.players if pyo.value(model.is_starter[i]) == 1]

    squad = df.loc[squad_indices].copy()
    starters = df.loc[starter_indices].copy()
    bench = squad.drop(starter_indices).copy()

    position_order = ["GKP", "DEF", "MID", "FWD"]
    starters["Position"] = pd.Categorical(
        starters["Position"], categories=position_order, ordered=True
    )
    bench["Position"] = pd.Categorical(
        bench["Position"], categories=position_order, ordered=True
    )

    total_cost = float(squad["Price"].sum())
    total_score = float(starters["Final_Score"].sum())
    bank = float(100.0 - total_cost)

    return SquadSolution(
        success=True,
        starters=starters,
        bench=bench,
        squad=squad,
        enriched_df=df,
        total_score=round(total_score, 2),
        total_cost=round(total_cost, 1),
        bank=round(bank, 1),
    )


def forge_pyomo_squad(
    gameweek_dir: str,
    return_squad: bool = False,
    force_reforge: bool = False,
) -> bool | Tuple[bool, pd.DataFrame, pd.DataFrame]:
    """Sovereign Pyomo Engine disk harness for command-line gauntlets.

    Maintains 100% backwards compatibility with commander and CLI.
    """
    print("--- CHIMERA PYOMO ENGINE (V3 - SOVEREIGN TRINITY) ONLINE ---")

    final_form_path = f"{gameweek_dir}/fpl_master_database_FINAL_v5.csv"
    omniscient_path = f"{gameweek_dir}/fpl_master_database_OMNISCIENT.csv"
    set_piece_path = "set_pieces.csv"

    if not os.path.exists(omniscient_path):
        print(f"!!! CRITICAL FAILURE: '{omniscient_path}' not found. Aborting.")
        if return_squad:
            return False, pd.DataFrame(), pd.DataFrame()
        return False

    omniscient_df = pd.read_csv(omniscient_path)
    print(f"[+] Intelligence loaded. Analyzing {len(omniscient_df)} players.")
    print("[+] Summoning the GLPK Solver Demon in memory...")

    solution = solve_chimera_squad(omniscient_df, set_pieces_path=set_piece_path)

    if not solution.success:
        print("\n!!! FAILURE: An optimal PYOMO solution could not be found.")
        if return_squad:
            return False, pd.DataFrame(), pd.DataFrame()
        return False

    # Persist Final Form DB to disk for downstream tools (squad prophecy, etc.)
    solution.enriched_df.to_csv(final_form_path, index=False)

    print("\n" + "=" * 20 + " PYOMO SQUAD FORGED (V3 - TRINITY) " + "=" * 20)
    print("\n--- STARTING XI (Final Score Maximized) ---")
    cols_to_show = [
        "Surname",
        "Team",
        "Position",
        "Price",
        "Final_Score",
        "Effective_FDR_Horizon_5GW",
    ]
    print(
        solution.starters[cols_to_show]
        .sort_values(by=["Position", "Final_Score"], ascending=[True, False])
        .to_string(index=False)
    )

    print("\n--- BENCH (Potency & Cost Optimized) ---")
    print(
        solution.bench[cols_to_show]
        .sort_values(by=["Position", "Final_Score"], ascending=[True, False])
        .to_string(index=False)
    )

    print("\n-------------------------------------------")
    print(f"Total Squad Cost:          £{solution.total_cost:.1f}m")
    print(f"Projected Starting Score:    {solution.total_score:.2f}")
    print(f"Money in the Bank:         £{solution.bank:.1f}m")
    print("-------------------------------------------")

    if return_squad:
        return True, solution.starters, solution.bench
    return True


if __name__ == "__main__":
    forge_pyomo_squad("gw3")

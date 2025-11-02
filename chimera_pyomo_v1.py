import pandas as pd
import pyomo.environ as pyo
import os
import sys

# --- Configuration (Mirrors the v5 Pulp script for parity testing) ---
# We will use the final, perfected database from our last successful run
FINAL_FORM_DB_PATH_V5 = (
    "gw6/fpl_master_database_FINAL_v5.csv"  # Using the known-good gw6 data for our test
)
THRIFT_FACTOR = 0.001


def forge_pyomo_squad(data_path: str):
    """
    The New Heart. Forges the optimal squad using the Pyomo framework.
    This function is a direct translation of the v5 pulp logic.
    """
    print("--- CHIMERA PYOMO ENGINE (V1 - HEART TRANSPLANT) ONLINE ---")
    if not os.path.exists(data_path):
        print(
            f"!!! CRITICAL FAILURE: Final Form Database not found at '{data_path}'. Aborting."
        )
        return False

    players_df = pd.read_csv(data_path)
    print(f"[+] Intelligence loaded. Analyzing {len(players_df)} players.")

    # --- 1. Model Initialization ---
    model = pyo.ConcreteModel(name="FPL_Pyomo_Chimera")
    print("[+] Pyomo ConcreteModel initialized.")

    # --- 2. Data Preparation & Set Definition (The Pyomo Way) ---
    # Pyomo thinks in Sets and Parameters, not just DataFrames. We feed the beast.
    player_indices = players_df.index.tolist()
    model.players = pyo.Set(initialize=player_indices)

    # Convert DataFrame columns into dictionaries for Pyomo Parameters
    final_scores = players_df["Final_Score"].to_dict()
    prices = players_df["Price"].to_dict()
    positions = players_df["Position"].to_dict()
    teams = players_df["Team_TLA"].to_dict()

    print("[+] Sets (players) and Parameters (scores, prices, etc.) defined.")

    # --- 3. Define the Decision Variables ---
    model.in_squad = pyo.Var(
        model.players, within=pyo.Binary, doc="Is player in the 15-man squad?"
    )
    model.is_starter = pyo.Var(
        model.players, within=pyo.Binary, doc="Is player in the 11-man starting XI?"
    )
    print("[+] Dual-layer decision variables created.")

    # --- 4. Define The Prime Directive (The Objective Function) ---
    def objective_rule(m):
        starter_score = sum(final_scores[i] * m.is_starter[i] for i in m.players)
        bench_penalty = sum(
            (m.in_squad[i] - m.is_starter[i]) * prices[i] * THRIFT_FACTOR
            for i in m.players
        )
        return starter_score - bench_penalty

    model.objective = pyo.Objective(
        rule=objective_rule, sense=pyo.maximize, doc="The Thrifty God Objective"
    )
    print("[+] Prime Directive (Thrifty God Objective) set.")

    # --- 5. Define The Chains of Reality (The Constraints) ---
    print("[+] Applying the Chains of Reality (Game Constraints)...")

    # SQUAD Constraints
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

    # Team Constraint (more elegant in Pyomo)
    model.team_list = pyo.Set(initialize=players_df["Team_TLA"].unique())

    def team_limit_rule(m, team_tla):
        return sum(m.in_squad[i] for i in m.players if teams[i] == team_tla) <= 3

    model.team_limit = pyo.Constraint(model.team_list, rule=team_limit_rule)

    # STARTER Constraints
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

    # The Logical Bridge
    def bridge_rule(m, i):
        return m.is_starter[i] <= m.in_squad[i]

    model.bridge = pyo.Constraint(model.players, rule=bridge_rule)

    print("[+] All constraints are locked in.")

    # --- 6. Unleash the New Beast (Solve the Problem) ---
    print("\n>>> Summoning the GLPK Solver Demon...")
    solver = pyo.SolverFactory("glpk")
    result = solver.solve(model, tee=False)  # tee=True shows solver output

    print(f">>> SOLVER TERMINATED. Status: {result.solver.termination_condition}")

    # --- 7. Reveal the New Chimera (Parse and Print Results) ---
    if result.solver.termination_condition == pyo.TerminationCondition.optimal:
        squad_indices = [i for i in model.players if pyo.value(model.in_squad[i]) == 1]
        starter_indices = [
            i for i in model.players if pyo.value(model.is_starter[i]) == 1
        ]

        squad = players_df.loc[squad_indices]
        starters = players_df.loc[starter_indices]
        bench = squad.drop(starter_indices)

        # ... (Identical printing logic from the v5 script) ...
        print("\n" + "=" * 20 + " PYOMO SQUAD FORGED (V1) " + "=" * 20)
        print("\n--- STARTING XI (Final Score Maximized) ---")
        print(
            starters[["Surname", "Team", "Position", "Price", "Final_Score"]]
            .sort_values(by=["Position", "Final_Score"], ascending=[True, False])
            .to_string(index=False)
        )
        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(
            bench[["Surname", "Team", "Position", "Price", "Final_Score"]]
            .sort_values(by=["Position", "Price"])
            .to_string(index=False)
        )
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:          £{squad['Price'].sum():.1f}m")
        print(f"Projected Starting Score:    {starters['Final_Score'].sum():.2f}")
        print(f"Money in the Bank:         £{100.0 - squad['Price'].sum():.1f}m")
        print("-------------------------------------------")
        return True
    else:
        print("\n!!! FAILURE: An optimal PYOMO solution could not be found.")
        return False


if __name__ == "__main__":
    forge_pyomo_squad(FINAL_FORM_DB_PATH_V5)

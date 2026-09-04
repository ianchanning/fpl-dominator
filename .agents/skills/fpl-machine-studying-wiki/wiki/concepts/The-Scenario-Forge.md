# The Scenario Forge & Multi-Scenario Stability Matrix (RFC-008)

## 1. The Sovereign Law
Quantify asset selection robustness across diverse temporal horizons and fixture weighting scenarios by running decoupled, in-memory Mixed-Integer Linear Programs (MILP) and synthesizing starting XI stability matrices with diff-first noise suppression.

---

## 2. The Trigger & Context
Standard FPL optimization pipelines evaluate a single static parameterization (e.g., fixed exponential decay rate $\lambda=0.7$ over 5 gameweeks). This creates dangerous systemic vulnerabilities:
- **Parameter Fragility:** A squad selected at $\lambda=0.7$ may be drastically sub-optimal if reality favors immediate returns ($\lambda=0.0$) or long-term structural reinvestment ($\lambda=1.0$).
- **Disk Collision & State Contamination:** Naive multi-scenario runners overwrite master databases (e.g., `fpl_master_database_FINAL_v5.csv`) during concurrent or sequential solves, corrupting intermediate pipeline state.
- **Cognitive Fog:** Comparing raw 15-man squad lists across 5 to 9 scenarios generates visual overload. Unchanging bench fodder (£4.0m backup goalkeepers and bench defenders) drowns out critical starting XI trade-offs.

The **Scenario Forge** (RFC-008) resolves these failures by decoupling solver memory from disk I/O, executing parametric matrices in RAM, and rendering high-contrast, diff-first stability grids.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Dynamic Multi-Run Chaos | Scenario Forge Architecture |
| :--- | :--- | :--- |
| **Solver Execution** | Shell loops invoking disk-writing CLI commands; constant disk thrashing and race conditions. | **Pure In-Memory Solves:** `solve_chimera_squad` executes entirely in RAM using GLPK, returning immutable `SquadSolution` dataclasses. |
| **Asset Robustness** | Subjective inspection of separate spreadsheet tabs or printed lists. | **Deterministic Robustness Score:** $R(p) = \frac{\text{Starter Appearances}}{\text{Total Solves}} \in [0.0, 1.0]$. |
| **Visual Signal-to-Noise** | Walls of repeated 15-player squad dumps. | **Diff-First Noise Suppression:** Automatically strips static bench anchors and badges starting alterations with `[X]*`. |
| **Reproducibility** | Undocumented parameter weights scattered across command-line flags. | **Weight Registry Footer:** Deterministic source-of-truth registry mapping every scenario signature to its vector $\mathbf{W}(t)$. |

---

## 4. The Implementation Pattern

### ❌ WRONG: Imperative Shell Loops & Disk Collisions
```python
# Anti-Pattern: Overwriting disk files and parsing output text
for decay in [0.4, 0.6, 0.8]:
    # Mutates global config file on disk
    update_config_decay(decay)
    # Overwrites fpl_master_database_FINAL_v5.csv on disk!
    os.system("bamf solve gw3")
    # Brittle text parsing of output files
    results.append(read_squad_from_csv("gw3/squad.csv"))
```

### ✅ RIGHT: Pure In-Memory Parameter Exploration (`scenario_forge.py`)
```python
from fpl_dominator.chimera_pyomo_v2 import solve_chimera_squad
from fpl_dominator.grand_synthesis import synthesize_omniscient_data
from fpl_dominator.scenario_forge import ScenarioDefinition, run_scenario_matrix

# 1. Define immutable scenario parameterization
scenarios = [
    ScenarioDefinition(
        name="EXP:0.75",
        model_type="exponential",
        param_value=0.75,
        weights=[1.0, 0.75, 0.56, 0.42, 0.32],
        form_factor_weight=0.7,
    ),
    ScenarioDefinition(
        name="EXP:0.25",
        model_type="exponential",
        param_value=0.25,
        weights=[1.0, 0.25, 0.06, 0.02, 0.00],
        form_factor_weight=0.7,
    ),
]

# 2. Execute zero-IO matrix solve in RAM
report = run_scenario_matrix("gw3", scenarios=scenarios, write_report=True)

# 3. Output diff-first terminal matrix with ANSI rainbow styling
print(
    report.to_terminal(
        suppress_static_bench=True, highlight_divergence=True, color=True
    )
)
```

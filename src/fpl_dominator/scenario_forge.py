"""Scenario Forge Matrix Builder and Parameter Generators.

Implements ScenarioDefinition and generators for multi-dimensional Cartesian exploration
(RFC-008) and single-axis parameter gradients (RFC-009) to map player survival curves.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

import pandas as pd
import yaml

from .chimera_pyomo_v2 import SquadSolution, solve_chimera_squad
from .grand_synthesis import synthesize_omniscient_data
from .temporal_decay import (
    generate_exponential_weights,
    generate_linear_weights,
    generate_scenario_signature,
    generate_step_weights,
    interpolate_gradient,
)


@dataclass(frozen=True)
class ScenarioDefinition:
    """Represents a single scenario parameterization in the Scenario Forge.

    Attributes:
        name: Compact unique scenario identifier / signature (e.g., 'EXP:0.75').
        model_type: Decay model archetype ('exponential', 'linear', 'step', 'flat').
        param_value: Numerical parameter value (decay_rate, slope, or cutoff).
        weights: List of fixture horizon weights W(t).
        form_factor_weight: Optional form weighting multiplier
            (None = use config default).
    """

    name: str
    model_type: str
    param_value: float
    weights: list[float]
    form_factor_weight: float | None = None

    def __post_init__(self) -> None:
        """Validates scenario integrity and mathematical invariants."""
        if not self.name or not self.name.strip():
            raise ValueError("Scenario name cannot be empty")
        if not self.model_type or not self.model_type.strip():
            raise ValueError("Scenario model_type cannot be empty")
        if not self.weights:
            raise ValueError("Scenario weights cannot be empty")
        for w in self.weights:
            if w < 0.0:
                raise ValueError(f"Scenario weight cannot be negative, got {w}")
        if self.form_factor_weight is not None and self.form_factor_weight < 0.0:
            raise ValueError(
                f"Form factor weight must be non-negative, got "
                f"{self.form_factor_weight}"
            )


def compute_scenario_weights(
    model_type: str, param_value: float, horizon: int = 5
) -> list[float]:
    """Computes fixture weights for a given decay model archetype and parameter.

    Args:
        model_type: Decay model ('exponential', 'linear', 'step', 'flat').
        param_value: Model parameter (decay_rate for exp, slope for lin,
            cutoff for step).
        horizon: Temporal fixture horizon length (default: 5).

    Returns:
        List of computed float weights for t = 0 .. horizon-1.

    Raises:
        ValueError: If model_type is unknown or parameters are invalid.
    """
    clean_model = model_type.strip().lower()
    if clean_model in ("exponential", "exp"):
        return generate_exponential_weights(decay_rate=param_value, horizon=horizon)
    if clean_model in ("linear", "lin"):
        return generate_linear_weights(slope=param_value, horizon=horizon)
    if clean_model in ("step", "horizon"):
        return generate_step_weights(cutoff=int(param_value), horizon=horizon)
    if clean_model in ("flat", "constant"):
        if horizon < 1:
            raise ValueError(f"Horizon must be >= 1, got {horizon}")
        return [1.0] * horizon

    raise ValueError(
        f"Unsupported decay model '{model_type}'. "
        f"Supported models: 'exponential', 'linear', 'step', 'flat'."
    )


def create_scenario(
    model_type: str,
    param_value: float,
    horizon: int = 5,
    form_factor_weight: float | None = None,
    name: str | None = None,
) -> ScenarioDefinition:
    """Factory helper to construct a validated ScenarioDefinition.

    If name is None, it is automatically derived via generate_scenario_signature.

    Args:
        model_type: Decay model ('exponential', 'linear', 'step', 'flat').
        param_value: Parameter value for the model.
        horizon: Temporal fixture horizon length (default: 5).
        form_factor_weight: Optional form factor weight modifier.
        name: Optional explicit scenario name.

    Returns:
        Validated ScenarioDefinition instance.
    """
    clean_model = model_type.strip().lower()
    weights = compute_scenario_weights(clean_model, param_value, horizon=horizon)
    scenario_name = name or generate_scenario_signature(
        clean_model, param_value, form_weight=form_factor_weight
    )
    return ScenarioDefinition(
        name=scenario_name,
        model_type=clean_model,
        param_value=param_value,
        weights=weights,
        form_factor_weight=form_factor_weight,
    )


def generate_cartesian_matrix(
    decay_rates: Sequence[float] = (0.4, 0.6, 0.8),
    form_factor_weights: Sequence[float | None] = (0.5, 0.7, 0.9),
    model_type: str | Sequence[str] = "exponential",
    horizon: int = 5,
    param_values: Sequence[float] | None = None,
) -> list[ScenarioDefinition]:
    """Generates Cartesian product scenarios across parameter dimensions.

    Explores multi-dimensional grid of (decay_rate x form_factor_weight)
    as specified in RFC-008.

    Args:
        decay_rates: Sequence of decay rates / parameter values to evaluate.
        form_factor_weights: Sequence of form factor multipliers (can include None).
        model_type: Model archetype string or sequence of archetype strings.
        horizon: Fixture horizon length (default: 5).
        param_values: Optional alias for decay_rates / parameter values.

    Returns:
        List of ScenarioDefinition instances covering all combinations.
    """
    models = [model_type] if isinstance(model_type, str) else list(model_type)
    values = list(param_values if param_values is not None else decay_rates)
    form_weights = list(form_factor_weights)

    scenarios: list[ScenarioDefinition] = []
    for m in models:
        for p in values:
            for fw in form_weights:
                scenarios.append(
                    create_scenario(
                        model_type=m,
                        param_value=float(p),
                        horizon=horizon,
                        form_factor_weight=fw,
                    )
                )
    return scenarios


def generate_gradient_matrix(
    model_type: str = "exponential",
    start: float = 1.0,
    end: float = 0.0,
    steps: int = 5,
    horizon: int = 5,
    form_factor_weight: float | None = None,
) -> list[ScenarioDefinition]:
    """Generates single-axis parameter gradient scenarios (RFC-009).

    Interpolates `steps` parameter values from `start` to `end` to map
    the selection survival curve.

    Args:
        model_type: Decay model archetype ('exponential', 'linear', 'step').
        start: Starting parameter extrema (e.g. 1.0 for Eternalist).
        end: Ending parameter extrema (e.g. 0.0 for Pure Sniper).
        steps: Total number of interpolated points (must be >= 2).
        horizon: Fixture horizon length (default: 5).
        form_factor_weight: Optional form factor weight modifier.

    Returns:
        List of ScenarioDefinition instances across the interpolated gradient.
    """
    clean_model = model_type.strip().lower()
    param_values = interpolate_gradient(start=start, end=end, steps=steps)

    return [
        create_scenario(
            model_type=clean_model,
            param_value=p,
            horizon=horizon,
            form_factor_weight=form_factor_weight,
        )
        for p in param_values
    ]


# Functional alias for parity with RFC documentation
generate_gradient_scenarios = generate_gradient_matrix


@dataclass(frozen=True)
class PlayerScenarioStats:
    """Aggregated scenario statistics and classification for an individual player.

    Attributes:
        surname: Player surname.
        position: Player position (GKP, DEF, MID, FWD).
        team: Player club short name or TLA.
        price: Player cost in millions.
        starter_appearances: Number of times selected in Starting XI.
        bench_appearances: Number of times selected on Bench.
        total_appearances: Total times selected in squad (starter + bench).
        robustness_score: Selection frequency in Starting XI (0.0 to 1.0).
        classification: Category ('IMMORTAL', 'HORIZON-DEPENDENT',
            'PURE PUNT', 'FRINGE', 'ROTATIONAL').
        scenario_selections: Mapping of scenario name to status indicator
            ('[X]', '[b]', '.').
    """

    surname: str
    position: str
    team: str
    price: float
    starter_appearances: int
    bench_appearances: int
    total_appearances: int
    robustness_score: float
    classification: str
    scenario_selections: Dict[str, str]


@dataclass(frozen=True)
class ScenarioRunReport:
    """Comprehensive report container for an executed Scenario Forge matrix.

    Contains all individual scenario solutions, aggregated player statistics,
    survival curve classifications, and formatting helpers.
    """

    gameweek_dir: str
    scenarios: List[ScenarioDefinition]
    solutions: Dict[str, SquadSolution]
    player_stats: List[PlayerScenarioStats]
    immortals: List[str]
    horizon_dependents: List[str]
    pure_punts: List[str]
    fringe: List[str]
    total_solves: int
    successful_solves: int

    def to_dataframe(self) -> pd.DataFrame:
        """Constructs a consolidated stability grid DataFrame."""
        records: List[Dict[str, object]] = []
        for p in self.player_stats:
            rec: Dict[str, object] = {
                "Surname": p.surname,
                "Position": p.position,
                "Team": p.team,
                "Price": p.price,
            }
            for sc in self.scenarios:
                rec[sc.name] = p.scenario_selections.get(sc.name, ".")
            rec["Robustness"] = f"{int(round(p.robustness_score * 100))}%"
            rec["Classification"] = p.classification
            records.append(rec)

        df = pd.DataFrame(records)
        if not df.empty:
            pos_order = {"GKP": 0, "DEF": 1, "MID": 2, "FWD": 3}
            df["pos_rank"] = df["Position"].map(pos_order).fillna(99)
            df["_rob_num"] = [p.robustness_score for p in self.player_stats]
            df.sort_values(
                by=["pos_rank", "_rob_num", "Price"],
                ascending=[True, False, False],
                inplace=True,
            )
            df.drop(columns=["pos_rank", "_rob_num"], inplace=True)
        return df

    def to_markdown(self) -> str:
        """Formats the stability matrix and strategic classification into Markdown."""
        df = self.to_dataframe()
        table_md = format_dataframe_to_markdown(df)

        imm_str = ", ".join(self.immortals) if self.immortals else "None"
        hor_str = (
            ", ".join(self.horizon_dependents) if self.horizon_dependents else "None"
        )
        punt_str = ", ".join(self.pure_punts) if self.pure_punts else "None"
        fringe_str = ", ".join(self.fringe) if self.fringe else "None"

        md_lines = [
            f"# Scenario Forge Analysis: {self.gameweek_dir.upper()}",
            "",
            f"**Total Scenarios Evaluated:** {self.total_solves} "
            f"({self.successful_solves} Successful)",
            "",
            "## Temporal Stability Matrix",
            "",
            table_md,
            "",
            "## Strategic Asset Classification",
            "",
            f"- **The Immortals ({len(self.immortals)} Locks):** {imm_str}",
            f"- **The Horizon-Dependents ({len(self.horizon_dependents)} Assets):** "
            f"{hor_str}",
            f"- **The Pure Punts ({len(self.pure_punts)} Assets):** {punt_str}",
            f"- **The Fringe / Volatile ({len(self.fringe)} Assets):** {fringe_str}",
            "",
            "## Weight Registry (Source of Truth)",
            "",
            "```text",
            "--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---",
        ]
        for sc in self.scenarios:
            weights_formatted = ", ".join(f"{w:.2f}" for w in sc.weights)
            md_lines.append(f"{sc.name:<10} -> [{weights_formatted}]")
        md_lines.extend(["```", ""])
        return "\n".join(md_lines)


def format_dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Converts a pandas DataFrame into standard GitHub Flavored Markdown table."""
    if df.empty:
        return "*Empty Matrix*"
    headers = [str(c) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(val) for val in row) + " |")
    return "\n".join(lines)


def classify_survival_curve(
    starter_scenarios: Set[str],
    all_scenarios: Sequence[ScenarioDefinition],
) -> Tuple[str, float]:
    """Classifies a player's survival curve based on selection across scenarios.

    Args:
        starter_scenarios: Set of scenario names where player was in Starting XI.
        all_scenarios: Full sequence of evaluated ScenarioDefinition instances.

    Returns:
        Tuple of (classification, robustness_score).
    """
    total = len(all_scenarios)
    if total == 0:
        return "UNSELECTED", 0.0

    selections = len(starter_scenarios)
    robustness = round(selections / total, 4)

    if selections == 0:
        return "UNSELECTED", 0.0

    if selections == total:
        return "IMMORTAL", robustness

    depths = {s.name: sum(s.weights) for s in all_scenarios}
    max_depth = max(depths.values())
    min_depth = min(depths.values())

    if max_depth == min_depth:
        return "ROTATIONAL", robustness

    deepest_scenarios = {name for name, d in depths.items() if d == max_depth}
    shallowest_scenarios = {name for name, d in depths.items() if d == min_depth}

    in_deepest = bool(starter_scenarios & deepest_scenarios)
    in_shallowest = bool(starter_scenarios & shallowest_scenarios)

    if in_deepest and not in_shallowest:
        return "HORIZON-DEPENDENT", robustness
    if not in_deepest and in_shallowest:
        return "PURE PUNT", robustness

    return "FRINGE", robustness


def run_scenario_matrix(
    gameweek_dir: str,
    scenarios: Sequence[ScenarioDefinition],
    set_pieces_path: str = "set_pieces.csv",
    config_path: str = "config.yaml",
    output_path: Optional[str] = None,
) -> ScenarioRunReport:
    """Executes an ensemble of scenarios in memory and aggregates stability metrics.

    Args:
        gameweek_dir: Directory containing prophetic and fixture CSV databases.
        scenarios: Sequence of ScenarioDefinition instances to evaluate.
        set_pieces_path: Path to set pieces CSV database.
        config_path: Path to config.yaml for base solver parameters.
        output_path: Optional path to write Markdown summary report.

    Returns:
        ScenarioRunReport containing full solutions, statistics, and classifications.

    Raises:
        ValueError: If scenarios sequence is empty.
        FileNotFoundError: If required source CSVs do not exist.
    """
    if not scenarios:
        raise ValueError("Scenario sequence cannot be empty")

    prophetic_path = os.path.join(gameweek_dir, "fpl_master_database_prophetic.csv")
    fixtures_path = os.path.join(gameweek_dir, "fixtures.csv")

    if not os.path.exists(prophetic_path):
        raise FileNotFoundError(f"Prophetic database not found at '{prophetic_path}'")
    if not os.path.exists(fixtures_path):
        raise FileNotFoundError(f"Fixture database not found at '{fixtures_path}'")

    players_df = pd.read_csv(prophetic_path)
    fixtures_df = pd.read_csv(fixtures_path)

    base_solver_config: Dict[str, object] = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
                if isinstance(cfg, dict):
                    base_solver_config = cfg.get("pyomo_solver", {}) or {}
        except (yaml.YAMLError, OSError):
            base_solver_config = {}

    solutions: Dict[str, SquadSolution] = {}
    player_starters_map: Dict[str, Set[str]] = {}
    player_bench_map: Dict[str, Set[str]] = {}
    player_info: Dict[str, Dict[str, object]] = {}

    successful_scenarios: List[ScenarioDefinition] = []

    for sc in scenarios:
        omniscient_df = synthesize_omniscient_data(
            players_df=players_df,
            fixtures_df=fixtures_df,
            fixture_weights=sc.weights,
        )

        solver_cfg = dict(base_solver_config)
        if sc.form_factor_weight is not None:
            solver_cfg["form_factor_weight"] = sc.form_factor_weight

        sol = solve_chimera_squad(
            omniscient_df=omniscient_df,
            set_pieces_path=set_pieces_path,
            solver_config=solver_cfg,
        )

        solutions[sc.name] = sol
        if not sol.success:
            continue

        successful_scenarios.append(sc)

        for _, row in sol.starters.iterrows():
            surname = str(row["Surname"])
            player_starters_map.setdefault(surname, set()).add(sc.name)
            if surname not in player_info:
                player_info[surname] = {
                    "Surname": surname,
                    "Position": row["Position"],
                    "Team": row["Team"],
                    "Price": float(row["Price"]),
                }

        for _, row in sol.bench.iterrows():
            surname = str(row["Surname"])
            player_bench_map.setdefault(surname, set()).add(sc.name)
            if surname not in player_info:
                player_info[surname] = {
                    "Surname": surname,
                    "Position": row["Position"],
                    "Team": row["Team"],
                    "Price": float(row["Price"]),
                }

    # Aggregate stats for each player
    player_stats_list: List[PlayerScenarioStats] = []
    immortals: List[str] = []
    horizon_dependents: List[str] = []
    pure_punts: List[str] = []
    fringe: List[str] = []

    for surname, info in player_info.items():
        starters_set = player_starters_map.get(surname, set())
        bench_set = player_bench_map.get(surname, set())

        classification, robustness = classify_survival_curve(
            starter_scenarios=starters_set,
            all_scenarios=successful_scenarios,
        )

        selections: Dict[str, str] = {}
        for sc in scenarios:
            if sc.name in starters_set:
                selections[sc.name] = "[X]"
            elif sc.name in bench_set:
                selections[sc.name] = "[b]"
            else:
                selections[sc.name] = "."

        stats = PlayerScenarioStats(
            surname=surname,
            position=str(info["Position"]),
            team=str(info["Team"]),
            price=float(info["Price"]),
            starter_appearances=len(starters_set),
            bench_appearances=len(bench_set),
            total_appearances=len(starters_set) + len(bench_set),
            robustness_score=robustness,
            classification=classification,
            scenario_selections=selections,
        )
        player_stats_list.append(stats)

        if classification == "IMMORTAL":
            immortals.append(surname)
        elif classification == "HORIZON-DEPENDENT":
            horizon_dependents.append(surname)
        elif classification == "PURE PUNT":
            pure_punts.append(surname)
        elif classification in ("FRINGE", "ROTATIONAL"):
            fringe.append(surname)

    # Sort players by position and robustness
    pos_order = {"GKP": 0, "DEF": 1, "MID": 2, "FWD": 3}
    player_stats_list.sort(
        key=lambda p: (
            pos_order.get(p.position, 99),
            -p.robustness_score,
            -p.price,
        )
    )

    report = ScenarioRunReport(
        gameweek_dir=gameweek_dir,
        scenarios=list(scenarios),
        solutions=solutions,
        player_stats=player_stats_list,
        immortals=sorted(immortals),
        horizon_dependents=sorted(horizon_dependents),
        pure_punts=sorted(pure_punts),
        fringe=sorted(fringe),
        total_solves=len(scenarios),
        successful_solves=len(successful_scenarios),
    )

    if output_path is not None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report.to_markdown())

    return report


__all__ = [
    "PlayerScenarioStats",
    "ScenarioDefinition",
    "ScenarioRunReport",
    "classify_survival_curve",
    "compute_scenario_weights",
    "create_scenario",
    "format_dataframe_to_markdown",
    "generate_cartesian_matrix",
    "generate_gradient_matrix",
    "generate_gradient_scenarios",
    "run_scenario_matrix",
]

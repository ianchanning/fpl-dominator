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

    @property
    def is_static_bench(self) -> bool:
        """Indicates if player is purely on the bench across all evaluated scenarios."""
        return self.starter_appearances == 0 and all(
            status == "[b]" for status in self.scenario_selections.values()
        )

    @property
    def is_divergent_starter(self) -> bool:
        """Indicates if player starts in some scenarios but not all (0 < R < 1.0)."""
        return 0.0 < self.robustness_score < 1.0


def filter_static_bench_players(
    players: Sequence[PlayerScenarioStats],
) -> List[PlayerScenarioStats]:
    """Filters out bench players that do not change across scenarios (RFC-008).

    Removes players who never appear in the Starting XI and whose status
    remains '[b]' across all evaluated scenarios.
    """
    return [p for p in players if not p.is_static_bench]


def highlight_starting_alterations(
    scenario_selections: Dict[str, str],
    robustness_score: float,
    divergence_marker: str = "*",
) -> Dict[str, str]:
    """Applies visual divergence cues to starting XI alterations.

    For non-immortal starters (0 < R < 1.0), marks '[X]' as '[X]*'
    (or custom divergence marker).
    """
    if not (0.0 < robustness_score < 1.0):
        return dict(scenario_selections)

    return {
        sc_name: (f"[X]{divergence_marker}" if status == "[X]" else status)
        for sc_name, status in scenario_selections.items()
    }


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

    @property
    def static_bench_players(self) -> List[str]:
        """List of player surnames who are purely static bench fodder."""
        return sorted([p.surname for p in self.player_stats if p.is_static_bench])

    @property
    def divergent_starters(self) -> List[str]:
        """List of player surnames who start in some but not all scenarios."""
        return sorted([p.surname for p in self.player_stats if p.is_divergent_starter])

    def filter_players(
        self,
        suppress_static_bench: bool = False,
        suppress_all_bench: bool = False,
        divergent_only: bool = False,
    ) -> List[PlayerScenarioStats]:
        """Filters player stats according to diff-first noise suppression criteria."""
        filtered = self.player_stats
        if suppress_all_bench:
            filtered = [p for p in filtered if p.starter_appearances > 0]
        elif suppress_static_bench:
            filtered = filter_static_bench_players(filtered)
        if divergent_only:
            filtered = [p for p in filtered if p.is_divergent_starter]
        return list(filtered)

    def to_dataframe(
        self,
        suppress_static_bench: bool = False,
        suppress_all_bench: bool = False,
        highlight_divergence: bool = False,
        divergence_marker: str = "*",
    ) -> pd.DataFrame:
        """Constructs a consolidated stability grid DataFrame.

        Args:
            suppress_static_bench: If True, filters out unchanging bench fodder.
            suppress_all_bench: If True, filters out all pure bench players.
            highlight_divergence: If True, marks altered starting slots.
            divergence_marker: Suffix appended to [X] for starting alterations.
        """
        records: List[Dict[str, object]] = []
        players = self.filter_players(
            suppress_static_bench=suppress_static_bench,
            suppress_all_bench=suppress_all_bench,
        )

        for p in players:
            rec: Dict[str, object] = {
                "Surname": p.surname,
                "Position": p.position,
                "Team": p.team,
                "Price": p.price,
            }
            selections = (
                highlight_starting_alterations(
                    p.scenario_selections,
                    p.robustness_score,
                    divergence_marker=divergence_marker,
                )
                if highlight_divergence
                else p.scenario_selections
            )
            for sc in self.scenarios:
                rec[sc.name] = selections.get(sc.name, ".")
            rec["Robustness"] = f"{int(round(p.robustness_score * 100))}%"
            rec["Classification"] = p.classification
            records.append(rec)

        df = pd.DataFrame(records)
        if not df.empty:
            pos_order = {"GKP": 0, "DEF": 1, "MID": 2, "FWD": 3}
            df["pos_rank"] = df["Position"].map(pos_order).fillna(99)
            rob_map = {p.surname: p.robustness_score for p in players}
            df["_rob_num"] = df["Surname"].map(rob_map).fillna(0.0)
            df.sort_values(
                by=["pos_rank", "_rob_num", "Price"],
                ascending=[True, False, False],
                inplace=True,
            )
            df.drop(columns=["pos_rank", "_rob_num"], inplace=True)
        return df

    def to_markdown(
        self,
        suppress_static_bench: bool = False,
        suppress_all_bench: bool = False,
        highlight_divergence: bool = False,
        divergence_marker: str = "*",
    ) -> str:
        """Formats the stability matrix and strategic classification into Markdown."""
        df = self.to_dataframe(
            suppress_static_bench=suppress_static_bench,
            suppress_all_bench=suppress_all_bench,
            highlight_divergence=highlight_divergence,
            divergence_marker=divergence_marker,
        )
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
        ]

        if highlight_divergence:
            md_lines.extend(
                [
                    f"*Legend:* `[X]` = Unanimous Starter | "
                    f"`[X]{divergence_marker}` = Starting Alteration | "
                    f"`[b]` = Bench | `.` = Unselected",
                    "",
                ]
            )

        if suppress_static_bench and self.static_bench_players:
            bench_fodder_str = ", ".join(self.static_bench_players)
            md_lines.extend(
                [
                    f"*Diff-First Noise Suppression:* Filtered "
                    f"{len(self.static_bench_players)} static bench players "
                    f"({bench_fodder_str}).",
                    "",
                ]
            )

        md_lines.extend(
            [
                "## Strategic Asset Classification",
                "",
                f"- **The Immortals ({len(self.immortals)} Locks):** {imm_str}",
                f"- **The Horizon-Dependents "
                f"({len(self.horizon_dependents)} Assets):** {hor_str}",
                f"- **The Pure Punts ({len(self.pure_punts)} Assets):** {punt_str}",
                f"- **The Fringe / Volatile "
                f"({len(self.fringe)} Assets):** {fringe_str}",
                "",
                "## Weight Registry (Source of Truth)",
                "",
                "```text",
                format_weight_registry(self.scenarios),
                "```",
                "",
            ]
        )
        return "\n".join(md_lines)

    def to_terminal(
        self,
        suppress_static_bench: bool = True,
        suppress_all_bench: bool = False,
        highlight_divergence: bool = True,
        divergence_marker: str = "*",
    ) -> str:
        """Formats the stability matrix and weight registry for terminal CLI output."""
        df = self.to_dataframe(
            suppress_static_bench=suppress_static_bench,
            suppress_all_bench=suppress_all_bench,
            highlight_divergence=highlight_divergence,
            divergence_marker=divergence_marker,
        )
        table_ascii = format_ascii_matrix(df)

        imm_str = ", ".join(self.immortals) if self.immortals else "None"
        hor_str = (
            ", ".join(self.horizon_dependents) if self.horizon_dependents else "None"
        )
        punt_str = ", ".join(self.pure_punts) if self.pure_punts else "None"
        fringe_str = ", ".join(self.fringe) if self.fringe else "None"

        lines = [
            f"=== SCENARIO FORGE STABILITY MATRIX ({self.gameweek_dir.upper()}) ===",
            (
                f"Scenarios Evaluated: "
                f"{self.successful_solves}/{self.total_solves} successful"
            ),
            "",
            table_ascii,
            "",
        ]

        if highlight_divergence:
            lines.extend(
                [
                    f"Legend: [X] = Starter | [X]{divergence_marker} = Alteration | "
                    f"[b] = Bench | . = Unselected",
                    "",
                ]
            )

        if suppress_static_bench and self.static_bench_players:
            bench_str = ", ".join(self.static_bench_players)
            lines.extend(
                [
                    f"Diff-First: Filtered {len(self.static_bench_players)} "
                    f"static bench players ({bench_str}).",
                    "",
                ]
            )

        lines.extend(
            [
                "=" * 78,
                f"[*] THE IMMORTALS ({len(self.immortals)} Locks): {imm_str}",
                f"[*] HORIZON-DEPENDENTS ({len(self.horizon_dependents)}): {hor_str}",
                f"[*] PURE PUNTS ({len(self.pure_punts)}): {punt_str}",
                f"[*] FRINGE / VOLATILE ({len(self.fringe)}): {fringe_str}",
                "=" * 78,
                "",
                format_weight_registry(self.scenarios),
            ]
        )
        return "\n".join(lines)

    def write_markdown_report(
        self,
        output_path: Optional[str] = None,
        suppress_static_bench: bool = True,
        suppress_all_bench: bool = False,
        highlight_divergence: bool = True,
        divergence_marker: str = "*",
    ) -> str:
        """Writes detailed Scenario Forge Markdown report to disk.

        Defaults to '{gameweek_dir}/scenario_forge.md'.
        """
        target_path = output_path or os.path.join(
            self.gameweek_dir, "scenario_forge.md"
        )
        content = self.to_markdown(
            suppress_static_bench=suppress_static_bench,
            suppress_all_bench=suppress_all_bench,
            highlight_divergence=highlight_divergence,
            divergence_marker=divergence_marker,
        )
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return target_path


def format_weight_registry(scenarios: Sequence[ScenarioDefinition]) -> str:
    """Builds the Weight Registry Footer (Source of Truth) for terminal and markdown."""
    lines = [
        "--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---",
    ]
    max_name_len = max((len(s.name) for s in scenarios), default=8)
    for sc in scenarios:
        weights_str = ", ".join(f"{w:.2f}" for w in sc.weights)
        lines.append(f"{sc.name:<{max_name_len}}  -> [{weights_str}]")
    return "\n".join(lines)


def format_ascii_matrix(df: pd.DataFrame) -> str:
    """Formats a DataFrame into a clean, aligned plain-text ASCII table."""
    if df.empty:
        return "No players to display."

    columns = [str(col) for col in df.columns]
    col_widths = {col: len(col) for col in columns}
    for _, row in df.iterrows():
        for col in columns:
            val_str = str(row[col])
            if len(val_str) > col_widths[col]:
                col_widths[col] = len(val_str)

    header_line = "  ".join(f"{col:<{col_widths[col]}}" for col in columns)
    sep_line = "  ".join("-" * col_widths[col] for col in columns)
    lines = [header_line, sep_line]

    for _, row in df.iterrows():
        row_str = "  ".join(f"{str(row[col]):<{col_widths[col]}}" for col in columns)
        lines.append(row_str)

    return "\n".join(lines)


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
    write_report: bool = True,
    suppress_static_bench: bool = True,
    highlight_divergence: bool = True,
) -> ScenarioRunReport:
    """Executes an ensemble of scenarios in memory and aggregates stability metrics.

    Args:
        gameweek_dir: Directory containing prophetic and fixture CSV databases.
        scenarios: Sequence of ScenarioDefinition instances to evaluate.
        set_pieces_path: Path to set pieces CSV database.
        config_path: Path to config.yaml for base solver parameters.
        output_path: Optional explicit path to write Markdown report.
        write_report: Whether to write markdown report to disk (default: True).
        suppress_static_bench: Whether to filter unchanging bench players.
        highlight_divergence: Whether to apply visual alteration cues ([X]*).

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

    if write_report:
        report.write_markdown_report(
            output_path=output_path,
            suppress_static_bench=suppress_static_bench,
            highlight_divergence=highlight_divergence,
        )

    return report


__all__ = [
    "PlayerScenarioStats",
    "ScenarioDefinition",
    "ScenarioRunReport",
    "classify_survival_curve",
    "compute_scenario_weights",
    "create_scenario",
    "filter_static_bench_players",
    "format_ascii_matrix",
    "format_dataframe_to_markdown",
    "format_weight_registry",
    "generate_cartesian_matrix",
    "generate_gradient_matrix",
    "generate_gradient_scenarios",
    "highlight_starting_alterations",
    "run_scenario_matrix",
]

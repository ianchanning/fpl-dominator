# BAMF Dominator: Master Knowledge Curriculum & Source Ingestion Manifest

This document is the **Canonical Curriculum** for Machine Studying in the `fpl-dominator` codebase. It catalogs all raw theoretical texts, solver specifications, data pipeline protocols, and mathematical optimization models.

---

## Curriculum Status Matrix

- `[x]` = **Compiled:** Ingested into `wiki/raw/` and synthesized into at least one Sovereign Grimoire in `wiki/`.
- `[/]` = **Ingested:** Raw text present in `wiki/raw/`, awaiting synthesis.
- `[ ]` = **Pending:** Identified source to be fetched and ingested.

---

## 1. Machine Studying & External Memory Foundations (`cat:foundations`)
*The cognitive architecture of persistent agent memory and recursive language models.*

| Status | Title / Topic | Type | Link / Source | Key Concepts |
| :--- | :--- | :--- | :--- | :--- |
| `[x]` | **Machine Studying** | Theory / Thesis | `wiki/raw/machine-studying.md` | Expertise equation ($\text{Acc} / \text{Tokens}$), test-time scaling, self-compounding external memory |
| `[x]` | **The LLM Wiki Architecture** | Architecture | `wiki/raw/llm-wiki.md` | Karpathy's 3-layer wiki architecture, progressive disclosure retrieval loop |
| `[x]` | **Recursive Language Models (RLM)** | Paper / Spec | `wiki/raw/recursive-language-models.md` | Context offloading, external memory forging, autonomous subagent swarms |

---

## 2. Mathematical Optimization & MILP Formulations (`cat:optimization`)
*Mixed-Integer Linear Programming models for Fantasy Premier League squad selection.*

| Status | Title / Topic | Type | Link / Source | Key Concepts |
| :--- | :--- | :--- | :--- | :--- |
| `[/]` | **The Chimera Pyomo Formulation** | Code / Spec | `src/fpl_dominator/chimera_pyomo_v2.py` | Binary decision variables, budget equality, position quotas, 3-per-team constraints |
| `[/]` | **The Production Chimera Solver (v5)** | Code / Spec | `src/fpl_dominator/chimera_final_form_v5_production.py` | Multi-objective optimization, captain selection, bench penalty weighting |
| `[/]` | **BAMF-RFC-002: Strongly Typed Chimera** | RFC / Spec | `wiki/raw/specs/BAMF-RFC-002_TYPE_SAFETY.md` | Eliminating Pyomo dynamic attribute chaos, Typed Protocols, Linopy migration |
| `[ ]` | **Sertalp Cay FPL MILP Optimization Framework** | Paper / Research | [github.com/sertalpbilal/FPL-Optimization-Tools](https://github.com/sertalpbilal/FPL-Optimization-Tools) | Multi-period transfer optimization, rolling horizon discount factors |

---

## 3. Data Pipelines, Scraping & Feature Engineering (`cat:pipeline`)
*High-velocity HTML extraction, reality alignment, and temporal feature synthesis.*

| Status | Title / Topic | Type | Link / Source | Key Concepts |
| :--- | :--- | :--- | :--- | :--- |
| `[/]` | **BAMF-RFC-001: The RIP Protocol** | RFC / Spec | `wiki/raw/specs/BAMF-RFC-001_RIP.md` | High-speed clipboard OuterHTML extraction, zero-manual-entry ingestion |
| `[/]` | **Grand Synthesis Feature Engine** | Code / Spec | `src/fpl_dominator/grand_synthesis.py` | Expected points ($xP$), temporal fixture discounting, weighted attack/defense FDR |
| `[/]` | **Price Change Reality Alignment** | Code / Spec | `src/fpl_dominator/update_prices.py` | Aligning bank balance and selling prices against market prices |
| `[/]` | **Player & Fixture HTML Processors** | Code / Spec | `src/fpl_dominator/process_players_html.py` | BeautifulSoup/Regex table parsing, team name normalization, coordinate mapping |

---

## 4. CLI Automation & Operational Protocols (`cat:operations`)
*The BAMF command deck and weekly management rituals.*

| Status | Title / Topic | Type | Link / Source | Key Concepts |
| :--- | :--- | :--- | :--- | :--- |
| `[/]` | **The BAMF Command Deck** | CLI / Spec | `src/fpl_dominator/bamf.py` | Master Click CLI interface: `init`, `rip`, `finalize`, `run-gauntlet`, `audit` |
| `[/]` | **The Commander Orchestrator** | Code / Spec | `src/fpl_dominator/commander.py` | Pipeline execution orchestration, `squad_prophecy.md` generation |
| `[/]` | **Data Integrity Auditing** | Code / Spec | `src/fpl_dominator/audit_player_names_v3.py` | Team name aliasing, fuzzy player name matching, reality verification |

---

## 5. Architectural RFC Specifications (`cat:specs`)
*Foundational RFCs, solver evolution, and feature engineering specifications.*

| Status | Title / Topic | Type | Link / Source | Key Concepts |
| :--- | :--- | :--- | :--- | :--- |
| `[x]` | **RFC-001: The Temporal Lens** | RFC / Spec | `wiki/raw/specs/RFC-001_Temporal_Lens.md` | Weighted fixture difficulty decay over 5GW horizon; synthesized into `wiki/Temporal-Discounting-and-FDR.md` |
| `[x]` | **RFC-002: Automated HTML Ingestion** | RFC / Spec | `wiki/raw/specs/RFC-002_Automated_Ingestion.md` | RIP protocol OuterHTML clipboard extraction; synthesized into `wiki/The-BAMF-CLI-Ritual.md` |
| `[ ]` | **RFC-003: Trajectory Optimization** | RFC / Spec | `specs/RFC-003_Trajectory_Optimization.md` | Multi-period rolling horizon transfer friction and budget liquidity |
| `[x]` | **RFC-004: The Wildcard Trigger** | RFC / Spec | `wiki/raw/specs/RFC-004_Wildcard_Trigger.md` | Squad divergence thresholds for triggering Wildcard chip |
| `[/]` | **RFC-005: Bayesian Prior Calibration** | RFC / Spec | `specs/RFC-005_Bayesian_Prior_Calibration.md` | Process metrics decay; cold start baseline synthesized into `wiki/concepts/The-Cold-Start-and-Season-Transition.md` |
| `[ ]` | **RFC-006: Stochastic Expected Minutes** | RFC / Spec | `specs/RFC-006_Stochastic_Expected_Minutes.md` | Probabilistic minute distributions and rotation risk |
| `[ ]` | **RFC-007: Early Season Liquidity** | RFC / Spec | `specs/RFC-007_Early_Season_Liquidity.md` | Capital preservation and team value appreciation |
| `[x]` | **RFC-008: The Scenario Forge** | RFC / Spec | `wiki/raw/specs/RFC-008_Scenario_Forge.md` | In-memory Cartesian parameter exploration; synthesized into `wiki/concepts/The-Scenario-Forge.md` |
| `[x]` | **RFC-009: Temporal Gradients** | RFC / Spec | `wiki/raw/specs/RFC-009_Temporal_Archetypes.md` | Survival curve taxonomy (Immortals, Punts); synthesized into `wiki/concepts/Temporal-Gradients-and-Survival-Curves.md` |
| `[ ]` | **RFC-010: The Equation Audit** | RFC / Spec | `specs/RFC-010_Equation_Audit.md` | Final Score stress-testing and alternative formulation benchmarking |
| `[x]` | **RFC-011: The Retrospective Lens** | RFC / Spec | `wiki/raw/specs/RFC-011_Retrospective_Lens.md` | Fixture-adjusted form and efficiency; synthesized into `wiki/concepts/The-Retrospective-Lens-and-Contextual-Form.md` |

---

## Ingestion & Synthesis Protocols

1. **MILP Formulation Distillation:** When ingesting a solver script or mathematical paper, extract the mathematical objective function $\max \sum c_i x_i$ and the set of explicit linear inequality constraints $A x \le b$.
2. **Feature Engineering Invariants:** Explicitly document metric definitions ($xG$, $xA$, $ICT$, $FDR$), temporal decay functions ($w_t = \lambda^t$), and normalization rules.
3. **Operational Protocols:** Ensure every CLI ritual has a step-by-step verified workflow with explicit input and output artifacts.

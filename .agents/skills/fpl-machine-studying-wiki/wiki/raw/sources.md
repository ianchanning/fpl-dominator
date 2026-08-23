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

## Ingestion & Synthesis Protocols

1. **MILP Formulation Distillation:** When ingesting a solver script or mathematical paper, extract the mathematical objective function $\max \sum c_i x_i$ and the set of explicit linear inequality constraints $A x \le b$.
2. **Feature Engineering Invariants:** Explicitly document metric definitions ($xG$, $xA$, $ICT$, $FDR$), temporal decay functions ($w_t = \lambda^t$), and normalization rules.
3. **Operational Protocols:** Ensure every CLI ritual has a step-by-step verified workflow with explicit input and output artifacts.

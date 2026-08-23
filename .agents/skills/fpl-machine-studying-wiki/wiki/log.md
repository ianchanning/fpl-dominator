# BAMF Dominator Wiki Log

This file is an append-only timeline of all knowledge base updates, source ingestions, and synthesis milestones for the `fpl-dominator` Machine Studying Wiki.

---

## [2026-08-23] initialization | Seed Master Architecture & Core Grimoires
- Initialized `.agents/skills/fpl-machine-studying-wiki/` and symlinked root `wiki -> .agents/skills/fpl-machine-studying-wiki/wiki`.
- Ingested foundational Machine Studying papers (`llm-wiki.md`, `machine-studying.md`, `recursive-language-models.md`) and operational protocols (`BAMF-RFC-001_RIP.md`, `BAMF-RFC-002_TYPE_SAFETY.md`).
- Forged `SKILL.md` defining the 3-Layer Wiki Architecture, 4-Part Mental Model Distillation Schema, and Progressive Disclosure Retrieval Loop.
- Synthesized foundational Grimoires:
  - `wiki/The-Chimera-Optimization-Engine.md` (MILP 0-1 decision variables, budget, position quotas, and GLPK solver rules).
  - `wiki/The-BAMF-CLI-Ritual.md` (The RIP protocol, clipboard HTML extraction, and `bamf finalize` pipeline).
  - `wiki/Temporal-Discounting-and-FDR.md` (Weighted decay fixture difficulty calculations in `grand_synthesis.py`).
- Initialized `wiki/index.md` with master knowledge graph and peripheral vision links.

## [2026-08-23] feature | Season 2025/26 Archival & Multi-Season Rollover Protocol
- Tagged repository state with git tag `season-2025-26-final`.
- Relocated 22 historical gameweek vaults (`gw3`..`gw29`), screenshots, and extraction utilities into `archive/2025-26/`.
- Implemented `bamf archive-season <season_tag>` command in `src/fpl_dominator/bamf.py` for automated end-of-season archiving.
- Updated `.gitignore`, `README.md`, and `wiki/The-BAMF-CLI-Ritual.md` to establish the Season Rollover Protocol.

## [2026-08-23] synthesis | Codify Cold Start & Season Transition Protocol (P4)
- Synthesized `wiki/concepts/The-Cold-Start-and-Season-Transition.md` under 4-Part Mental Model.
- Formalized mathematical resolution of GW1 Total Points ($TP=0$) zero-singularity via decaying Bayesian prior baseline $\alpha_t \in [0, 1]$ over GW1–GW5.
- Documented data ingestion heterogeneity for prior season full-year HTML tables and unconstrained greenfield GW1 treasury state.
- Linked new node to `wiki/index.md` knowledge graph.

## [2026-08-23] ingestion | Ingest 2025/26 Aggregate HTML Dump & Forge Baseline Dataset
- Ingested `archive/2025-26/fpl_player_stats.html` (33,871 lines, dual-header schema).
- Forged `src/fpl_dominator/process_prior_season_html.py` equipped with dual-header decoding, `profile-title` position/club parsing, and historical fallback resolution.
- Extracted all 491 players to `archive/2025-26/fpl_player_stats_2025_26.csv` with calculated `Pts_per_90` and normalized canonical team TLAs.
- Added `bamf process-prior-season` to master CLI deck.

## [2026-08-23] refactor | Purge Legacy PuLP & Unify Sovereign Pyomo Engine
- Purged `pulp` from `pyproject.toml` dependencies.
- Consolidated `src/fpl_dominator/chimera_pyomo_v2.py` with standalone Set-Piece Potency enrichment and Final Score calculation.
- Streamlined `src/fpl_dominator/commander.py` to execute exclusively via Pyomo and GLPK solver (`glpsol`).
- Removed `chimera_final_form_v5_production.py` and archived `chimera_scenarios.py`.
- Unified solver configuration parameters in `config.yaml` under `pyomo_solver`.

## [2026-08-23] feature | Ingest 2025/26 Empirical Set Piece Volume & Automate Matrix Synthesis
- Ingested `archive/2025-26/set_pieces.html` (17,758 lines, 455 players with granular delivery metrics).
- Created `src/fpl_dominator/process_set_pieces_html.py` calculating per-90 corner, free kick, and penalty delivery rates.
- Generated `archive/2025-26/set_pieces_detailed_2025_26.csv` and derived empirical `set_pieces.csv` across all 20 Premier League clubs.
- Added `bamf process-set-pieces` command to CLI deck.





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
- Extracted all 491 players to `archive/2025-26/fpl_player_stats_2025_26 l.csv` with calculated `Pts_per_90` and normalized canonical team TLAs.
- Added `bamf process-prior-season` command to CLI deck.

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

## [2026-08-23] feature | Bayesian Prior Cold Start Synthesis & GW1 Finalization
- Implemented `inject_bayesian_prior_baseline()` in `src/fpl_dominator/enrich_with_insight.py` with dynamic decay $\alpha_t = \max(0, 1 - \frac{t-1}{5})$.
- Matched 156 historical players directly to 2025/26 actuals via normalized surname & position joining; imputed 47 new/promoted assets via position PPM benchmarks.
- Reconciled market prices defensively in `update_prices.py` and `process_players_html.py`.
- Successfully executed `bamf finalize gw1`, forging `gw1/squad_prophecy.md` and complete intermediate databases.

## [2026-08-23] config | Recalibrate Pantheon Captaincy Tiers & Harden Namesake Disambiguation
- Updated `config.yaml` with 2026/27 empirical hierarchy: Gods (`Haaland`, `B.Fernandes` @ `1.20x`), Demigods (`Semenyo`, `João Pedro`, `Gabriel`, `Saka`, `Palmer`, `Thiago` @ `1.08x`), purging Salah.
- Hardened `enrich_with_insight.py` with collision-resistant matching respecting initials (`B.Fernandes` vs `M.Fernandes`), club membership, and positional roles (`Cole Palmer` MID vs `Palmer` GKP).
- Finalized initial `gw2/` vault baseline with live GW2–GW6 fixture schedule.

## [2026-09-04] feature | Scenario Forge & Temporal Gradients Engine (RFC-008 & RFC-009)
- Implemented `src/fpl_dominator/temporal_decay.py` with pure functional exponential, linear, step, and flat fixture horizon weighting functions and gradient interpolation.
- Decoupled Pyomo MILP optimization engine in `chimera_pyomo_v2.py` introducing frozen `SquadSolution` dataclass and pure in-memory `solve_chimera_squad()`, eliminating multi-scenario disk collisions.
- Built `src/fpl_dominator/scenario_forge.py` supporting multi-dimensional Cartesian grid search (RFC-008) and continuous parameter gradients (RFC-009).
- Formulated Effective Horizon Depth $\Omega(s) = \sum W_s(t)$ and automated survival curve classification: Immortals ($R=1.0$), Horizon-Dependents, Pure Punts, and Fringe/Volatile.
- Implemented Diff-First noise suppression, visual starting alteration cues (`[X]*`), ASCII terminal formatters, ANSI rainbow color ramps, and automated markdown reports (`gwX/scenario_forge.md`).
- Integrated `bamf forge` command deck into `bamf.py` with `--matrix`, `--model`, `--param-range`, `--steps`, `--diff-first/--full`, and `--color/--no-color`.
- Empirically proved on active GW3 data that Bruno Fernandes (£12.0m, $R=100\%$) is an unconditional Immortal lock, whereas Erling Haaland (£15.5m, $R=60\%$) is a short-horizon Pure Punt.
- Synthesized Living Grimoire nodes `wiki/concepts/The-Scenario-Forge.md` and `wiki/concepts/Temporal-Gradients-and-Survival-Curves.md`, and updated `wiki/index.md`.

## [2026-09-12] feature | The Retrospective Lens & Form Fraud Detection (RFC-011)
- Implemented `src/fpl_dominator/retrospective_lens.py` providing pure extraction of historical fixture difficulties (`FDR_A` for attackers, `FDR_D` for defenders) and per-gameweek delta points from historical vaults.
- Fixed critical latent gremlin in `enrich_with_insight.py` that previously subtracted historical raw points from 38-game Bayesian annualized points; preserved `Raw_TP` defensively.
- Forged `Adjusted_Form` ($\sum \Delta \text{Pts} \times \frac{\text{FDR}_{\text{past}}}{1000.0}$) and `Form_Efficiency` ($\frac{\text{Actual}}{\text{Expected}}$) across all player intelligence databases.
- Parameterized `form_model` ('retrospective' vs 'raw') in `chimera_pyomo_v2.py` and `config.yaml`.
- Integrated `--compare-form` into `scenario_forge.py` and `bamf forge`, automated classification of **Form Frauds** and **Sleepers**.
- Empirically proved on active GW4 data: Ajayi (£4.1m, Hull City) unmasked as a **Form Fraud** (50% robustness, dropped under retrospective lens), while Van Hecke (£4.9m, Spurs) elevated as a **Sleeper** (promoted to Starting XI under retrospective lens).
- Synthesized Living Grimoire node `wiki/concepts/The-Retrospective-Lens-and-Contextual-Form.md` and updated `wiki/index.md`.

## [2026-09-12] protocol | Canonical RFC Archival Protocol & Layer 1 Ingestion
- Codified canonical RFC lifecycle: active proposals reside in `specs/`; completed/verified RFCs migrate into Layer 1 (`wiki/raw/specs/`) as immutable ground truth.
- Migrated completed RFCs (`RFC-001`, `RFC-002`, `RFC-004`, `RFC-008`, `RFC-009`, `RFC-011`) into `wiki/raw/specs/` via git history-preserving renames.
- Forged `specs/README.md` cataloging the RFC lifecycle and mapping active vs ingested RFCs.
- Updated `wiki/raw/sources.md` with Section 5 tracking all 11 architectural RFCs and linked in `wiki/index.md`.

## [2026-09-12] test | Dan Luu Testing Heuristics & Defensive Invariant Crucible
- Implemented comprehensive 14-test battery in `tests/test_retrospective_lens.py` following Dan Luu's Testing Heuristics.
- Established independent mathematical oracle re-derivation without production helpers or shared module state.
- Identified and exterminated critical fallback gremlin: snapshot missingness previously evaluated Bayesian annualized `TP` divided by lookback weeks, inflating un-snapshotted defenders (Mitchell, Van Hecke) to >220 Adjusted Form; fixed to `Raw_TP / max(1, current_gw - 1)`, vaulting Riccardo Calafiori to #1 starting Arsenal defender.
- Added structured property-based testing verifying non-negativity, parity identity ($FDR=1000 \implies \text{Form}=\text{Raw}$), monotonic difficulty scaling, and FDR $\le 800$ clamping.
- Verified real-world vault integration on `gw1`–`gw4` databases (Haaland 13pt haul delta in GW3).
- Updated `README.md` with Dan Luu testing methodology, architectural flowchart, and test manifest.

## [2025-01-23] recovery | Surgical Point Rewind & Look-Ahead Bias Purge
- Resolved critical data pollution in `gw7` vault where subsequent GW8 points had been ingested into historical totals.
- Developed a name-mapped subtraction protocol to excise GW8 GWP from GW7 TP without requiring full vault re-import.
- Forged `wiki/raw/point-rewind-recovery.py` as an immutable record of the recovery logic.
- Synthesized `wiki/concepts/Data-Integrity-and-Point-Rewind.md` detailing the "Surgical Purge" pattern and the danger of non-idempotent recovery scripts.
- Purged 61 affected players across 7 positional HTML files.
- Updated `wiki/index.md` and `wiki/log.md` to institutionalize the recovery protocol.

## [2026-10-18] feature | Automated Ingestion Pipeline & Dan Luu Contract Oracle (RFC-012)
- Formalized `specs/RFC-012_Pipeline.md` with end-to-end Mermaid sequence diagram, resilient React-Aria and FFS selectors, multi-page pagination protocols, and zero-leak secrets architecture.
- Forged `tests/test_ingest_contract.py` implementing an independent verification oracle and Dan Luu testing crucible; verified bit-parity on `gw7` and confirmed defect detection on `gw8`.
- Implemented `src/fpl_dominator/vault_contract.py` providing `verify_vault_contract()` and `assert_vault_contract()` invariant gates.
- Implemented `src/fpl_dominator/ingest_playwright.py` with OneTrust cookie dismissal, FPL/FFS credential handling, multi-page positional table harvesting, and atomic staging.
- Added `bamf fetch [gwX]` command to CLI deck and expanded `bamf rip` with `gkp2`.
- Deployed `.github/workflows/fpl_data_ingest.yml` for scheduled pre-deadline automated ingestion and commit-back.
- Diagnosed and resolved live portal friction: navigated Ping Identity SSO (`account.premierleague.com`) challenge redirects, neutralized late-injected OneTrust banners (`#onetrust-banner-sdk`) via asynchronous barriers, switched React ARIA radiogroup to List view, synchronized FFS Season Ticker to 5 GWs horizon (`37,311 bytes`), and verified 100% Invariant Contract Oracle pass.
- Executed live full gauntlet (`bamf finalize gw8`) on freshly harvested automated data, forging `gw8/squad_prophecy.md` via GLPK MILP solver; maintained 55 passing unit and contract tests in 3.4s.
- Synthesized Living Grimoire node `wiki/concepts/Automated-Data-Ingestion-and-Contract-Oracle.md` and indexed in `wiki/index.md`.

## [2026-10-18] feature | Modern Static Type Safety & The Ty Verification Gate (RFC-013)
- Forged `specs/RFC-013_Static_Type_Safety_With_Ty.md` formalizing zero-diagnostic static typing with Astral's `ty` Rust-based type checker.
- Eradicated 75 static typing diagnostics across `src/` and `tests/`:
  - Replaced Python built-in `sum()` over Pyomo expressions with `pyo.quicksum()`, resolving generator overload failures and speeding up linear expression tree generation.
  - Implemented `@overload` signatures for `forge_pyomo_squad()` enabling compile-time return shape narrowing (`bool` vs `Tuple[bool, DataFrame, DataFrame]`).
  - Switched `solver_config` parameter typing to covariant `Optional[Mapping[str, object]]` to support subtype dictionary parameters without variance friction.
  - Hardened config extraction with defensive `_get_float` and `_get_int` helpers and type validation.
  - Replaced Playwright `**context_kwargs` dynamic unpacking with explicit named parameters, eradicating 36 overload diagnostics.
  - Added type guards and assertions for environment credentials, BeautifulSoup attributes, table header tags, and CSV price string formatting.
  - Formalized `PlayerMetadata` TypedDict in `scenario_forge.py`.
- Integrated `ty` into `pyproject.toml` dev dependencies and updated `README.md` quality gates.
- Achieved **zero diagnostics** with `ty check src tests` while passing all 55 unit tests and ruff format/lint checks.

## [2026-10-18] test | Dan Luu Test Crucible & Rich Type Surface Expansion (RFC-013 & RFC-004)
- Enriched `SquadSolution` in `src/fpl_dominator/chimera_pyomo_v2.py` with rich, strongly-typed domain properties:
  - `formation`: Standard FPL starting formation string derived from starter position distribution (e.g., `'3-5-2'`, `'4-4-2'`).
  - `captain` / `vice_captain`: Strongly-typed surname properties resolving top-2 starters by `Final_Score`.
  - `position_costs`: Granular dictionary mapping position TLAs to expenditure across the 15-man squad.
  - `red_zone_starters`: Filtered list of starters facing fixture difficulty `FDR > 1250.0`.
  - Empty/undersized pool defense: Gracefully returns an unsuccessful `SquadSolution` when candidate pool has `< 15` players.
- Formalized `WildcardEvaluationResult` TypedDict in `src/fpl_dominator/wildcard_evaluator.py` documenting the complete 17-key contract for squad divergence analysis.
- Expanded `tests/test_in_memory_solver.py` (from 4 to 11 tests) applying Dan Luu Testing Heuristics:
  - **Principle 1 (Edge Cases):** Impossible astronomical budget infeasibility, empty and undersized (<15 players) DataFrame guard, string-coerced hyperparameter extraction, and unrecognized form model fallback.
  - **Principle 2 (Independent Oracle):** Implemented `_independently_verify_fpl_rules` verifying all 15 FPL combinatorial rules, subset/disjointness laws, positional quotas, 3-per-club ceilings, and budget conservation without Pyomo.
  - **Principle 3 (Property Invariants):** Validated `@overload` return signatures for `forge_pyomo_squad()` and rich domain properties.
- Forged `tests/test_wildcard_evaluator.py` (3 tests) covering the RFC-004 Wildcard Evaluator:
  - **Principle 1 (Edge Cases):** Missing vault directory `FileNotFoundError` handling.
  - **Principle 2 (Independent Oracle):** Implemented `_independently_rederived_wildcard_decision` independently re-deriving Path A (Hold), Path B (Mini-Wildcard), Path C (Wildcard Now), and dynamic threshold curves without production helpers.
  - **Principle 3 (Property Invariants):** Contract invariant verification on `WildcardEvaluationResult` ensuring formation validity and transfer conservation ($15 - \text{players\_to\_keep} = \text{transfers\_needed}$).
  - **Principle 4 (Real Vault):** Historical integration test against `gw3` production vault artifacts.
- Maintained **zero diagnostics** with `uv run ty check src tests`, zero Ruff lints, and 100% test pass rate across 65 tests in ~3.8s.



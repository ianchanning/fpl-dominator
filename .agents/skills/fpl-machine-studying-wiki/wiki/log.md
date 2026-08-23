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


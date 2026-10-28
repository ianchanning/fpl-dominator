# Container Runner Pitfalls (The Ghost Runner & The Invisible Venv)

## 1. The Sovereign Law

**A GitHub Actions `container:` job inherits *nothing* from the host runner image and no working-directory symlink to its Python environment — every binary the job needs (including `git`) must exist inside the image, and the baked venv must be made globally visible via `ENV VIRTUAL_ENV`, or steps that assume host-runner affordances fail with exit 127 or "No virtual environment found".**

## 2. Formulation & Trigger Context

RUD (run `40661580420`, 2026-10-28): after `23f1abd` switched `fpl_data_ingest.yml` to the pre-baked `ghcr.io/ianchanning/fpl-dominator-runner:latest` container, the first real job died at "Mark Workspace as Git Safe" with `git: not found` (exit 127). The container is `python:3.12-slim-bookworm` + `glpk-utils` + `ca-certificates` only.

Two coupled defects, the second invisible because the first killed the run early:

| # | Step | Assumption | Reality in container |
| --- | --- | --- | --- |
| 1 | `git config --global --add safe.directory ...` | `git` exists (true on bare `ubuntu-latest`) | `git` is **missing** → exit 127. Deeper: without git, `actions/checkout@v7` **silently falls back to a tarball download** (step still reports ✓), so the workspace has no `.git` dir and the later `git add/commit/push` "Commit & Push Harvested Vault" step *also* cannot work — the job's purpose is structurally broken, not just its safe.directory line |
| 2 | `uv pip install --no-deps -e .` ("Link Working Copy") | `uv` finds the project venv | Steps run with CWD `/github/workspace`; the venv is baked at `/app/.venv`; no `VIRTUAL_ENV` env var → `uv pip` aborts: `error: No virtual environment found` (reproduced locally, exit 2). Even a hypothetical auto-created workspace venv would *not* be on `PATH`, so `bamf` would silently execute the **stale image-baked** `/app/src` instead of the fresh checkout — a version-drift zombie |

Forensics on the shipping image (`docker run ... ghcr.io/ianchanning/fpl-dominator-runner:latest`): `git: MISSING`, `VIRTUAL_ENV: []`, while `uv`, `/app/.venv`, `glpsol` were all healthy. Last green ingest run (40062040180, 2026-10-24 04:21 UTC) *predates* the container switch (23f1abd, 06:20 UTC) — the containerized pipeline had never executed successfully before this RUD.

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| ❌ WRONG (host-runner cargo cult) | ✅ RIGHT (container-native reasoning) |
| --- | --- |
| "It worked on bare `ubuntu-latest`, so the same steps work in a container" | Container = different OS universe: no host `git`, no host `PATH`, no host `~/.cache`; audit the image, not the runner |
| Read the green ✓ on "Checkout Codebase" as proof git exists | Checkout success in a git-less image proves the **tarball fallback** fired; verify a real clone: `.git/` must exist for `commit/push` |
| Rely on `uv` venv auto-discovery (CWD walk-up for `.venv`) from an arbitrary CWD | Pin the environment **in the image**: `ENV VIRTUAL_ENV=/app/.venv` — deterministic for `uv pip`, `pip`, and bare `python` regardless of step CWD |
| Fix the single failed step and hope the next run fails further along | Rehearse the *entire* post-mortem step chain in the rebuilt image before shipping (dress rehearsal: git config → `uv pip install --no-deps -e .` → import path check) |

## 4. The Pattern

### ❌ WRONG (RUD 40661580420)

```dockerfile
# python:3.12-slim base, only solver dep installed — no VCS, no env pin
RUN apt-get update && apt-get install -y --no-install-recommends \
    glpk-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/app/.venv/bin:$PATH"   # PATH only: uv pip still cannot find the venv
```

```yaml
# workflow — assumes host-runner affordances
- name: Mark Workspace as Git Safe
  run: git config --global --add safe.directory "$GITHUB_WORKSPACE"   # -> 127
- name: Link Working Copy
  run: uv pip install --no-deps -e .                                  # -> no venv (exit 2)
```

### ✅ RIGHT (shipped fix, Dockerfile)

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/app/.venv        # pins uv/pip/python to the baked venv from any CWD

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \                         # checkout must produce a REAL clone (no tarball fallback); commit/push need VCS
    glpk-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```

**Verification protocol (apply to any container-image change):** `docker build -t <name>:fixtest .` locally, then replay the failing steps in a bind-mounted workspace:

```bash
docker run --rm --entrypoint sh \
  -v $PWD:/github/workspace -w /github/workspace <name>:fixtest -c '
    git --version
    git config --global --add safe.directory /github/workspace
    uv pip install --no-deps -e .
    python -c "import fpl_dominator; print(fpl_dominator.__file__)"   # must print WORKSPACE path, not /app path
'
```

The import-path assertion is the load-bearing check: it proves the editable re-link binds `fpl_dominator` to the fresh checkout, not the stale image-baked source.

## 5. Operational Notes

- Rebuild & republish via push to master — `docker_publish.yml` auto-triggers on `Dockerfile` changes (`latest` + short-sha tags), then re-dispatch `fpl_data_ingest.yml`.
- Related: [[GHCR-Provenance-Attestation-Gremlin]] (image publishing hygiene), [[Automated-Data-Ingestion-and-Contract-Oracle]] (the workflow this fix serves).
- Pre-existing drift (not this bug): `README.md` documents the ingest schedule as "Fridays 12:00 & 16:00 UTC" while the live cron is `0 12 * * 3` (Wed 12:00 UTC, single fire).
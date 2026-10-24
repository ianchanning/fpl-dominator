# UV-Ty Unified Toolchain Integration

> **Source:** [[raw/docs/uv-ty-integration-astral-blog-2026]] (Astral Blog, 2026)
> **RFC:** [[../specs/RFC-013_Static_Type_Safety_With_Ty]] (The Ty Verification Gate)
> **Status:** ✅ FULLY INTEGRATED (uv 0.13.5, ty 0.0.91)

---

## 1. The Sovereign Law

**Unify package management (`uv`), linting (`ruff`), and type checking (`ty`) into a single Astral toolchain where `uv check` orchestrates environment-aware static analysis with zero manual virtual environment coordination, and `[tool.ty]` in `pyproject.toml` declares typed invariants as code.**

---

## 2. The Formulation & Trigger Context

The BAMF Dominator already achieved **zero `ty` diagnostics** (RFC-013) across `src/` and `tests/`, but the integration is fragile and manually wired:

- **Disconnected invocation:** `uv run ty check src tests` is a manual shelling-out pattern — `uv` runs `ty` as a subprocess but doesn't share workspace metadata, dependency resolution, or Python version constraints with it.
- **Version drift:** `ty` is pinned as a dev dependency in `pyproject.toml` but the CI workflow invokes it via `uv run ty check` without lockfile-pinned binary guarantees. Different environments may run different `ty` versions.
- **No `[tool.ty]` configuration:** The project has zero `ty`-specific configuration in `pyproject.toml`. `ty check src tests` passes the include paths via CLI args. Excludes (archive, wiki, .agents) are implicit. Rule severities are unconfigured — all rules use their defaults.
- **Docker image gap:** The Dockerfile doesn't install dev dependencies, so `ty` checks can't run inside containers for CI reproducibility.
- **No pre-commit hook:** Type checking happens only when developers remember to run it manually or in CI.

### What the uv-ty Integration Unlocks

The Astral blog post (uv ≥ 0.12.3, ty ≥ 0.0.76) introduces:

1. **`uv check`** — a single command that auto-syncs the environment, resolves ty from the lockfile, and runs type checking. No manual `uv run ty check` invocation needed.
2. **`uv workspace metadata`** — structured project metadata sharing between uv and ty, enabling ty to understand the full dependency graph, Python version, and workspace layout.
3. **PEP 723 Script Support** — standalone Python scripts with inline `# /// script` metadata blocks get isolated ty environments automatically.
4. **Lockfile-pinned ty version** — `uv check` uses the exact ty version from `uv.lock`, ensuring CI/CD and developer machines run identical analysis.
5. **Pre-commit hook** — `astral-sh/ty-pre-commit` uses `uv check` under the hood for zero-config type checking on every commit.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | ❌ Current (Manual `uv run ty`) | ✅ Integrated (`uv check` + `[tool.ty]`) |
|---|---|---|
| **Invocation** | `uv run ty check src tests` (manual args) | `uv check` (reads `[tool.ty.src]` config) |
| **Version Pinning** | Dev dependency, but no binary lock guarantee | Lockfile-pinned via `uv.lock` |
| **Environment Awareness** | ty doesn't know about project dependencies | `uv workspace metadata` shares full dep graph |
| **Configuration** | CLI flags only, no declarative config | `[tool.ty]` in `pyproject.toml` (typed, version-controlled) |
| **CI Reproducibility** | `uv run ty check` may resolve different version | `uv check` always uses lockfile version |
| **Pre-commit** | None | `astral-sh/ty-pre-commit` hook |
| **Rule Granularity** | Default severity for everything | Per-rule `error`/`warn`/`ignore` in `[tool.ty.rules]` |
| **Test Overrides** | Tests checked with same strictness as src | `[[tool.ty.overrides]]` can relax rules for `tests/` |
| **Exclude Paths** | Implicit (only `src tests` passed) | Explicit `[tool.ty.src]` exclude patterns |

---

## 4. The Pattern (❌ WRONG vs. ✅ RIGHT)

### ❌ WRONG: Manual Invocation Without Configuration

```bash
# No config — paths hardcoded in CLI, no exclude patterns, no rule tuning
uv run ty check src tests

# README quality gate — fragile string of && operators
uv run ruff check . && uv run ruff format --check . && uv run ty check src tests
```

```toml
# pyproject.toml — ty exists only as a bare dependency
[project.optional-dependencies]
dev = ["ruff", "ty"]

# No [tool.ty] section at all
```

### ✅ RIGHT: Declarative Configuration + Unified Command

```toml
# pyproject.toml — ty configured as code alongside ruff
[project.optional-dependencies]
dev = ["ruff", "ty"]

[tool.ty.environment]
python-version = "3.10"  # Match requires-python floor

[tool.ty.src]
include = ["src", "tests"]
exclude = ["archive", ".agents", "wiki"]

[tool.ty.rules]
# Enforce all rules as errors by default for maximum strictness
# Selectively ignore rules that conflict with Pyomo's dynamic model patterns
"possibly-unresolved-reference" = "error"

[[tool.ty.overrides]]
include = ["tests/**"]
[tool.ty.overrides.rules]
# Tests may use broader assertions and dynamic patterns
"redundant-cast" = "ignore"
```

```bash
# Unified single command — resolves env, installs deps, runs ty from lockfile
uv check

# Or for CI — explicit workspace-wide check
uv check --all-packages

# Pre-commit hook runs uv check automatically on every commit
```

```yaml
# .pre-commit-config.yaml — zero-config type safety on commit
repos:
  - repo: https://github.com/astral-sh/ty-pre-commit
    rev: v0.0.89
    hooks:
      - id: ty
```

### Upgrade Path (BAMF Dominator Specific)

1. **Upgrade uv** from `0.11.6` → `≥ 0.12.3` (`uv self update`)
2. **Add `[tool.ty]`** configuration to `pyproject.toml`
3. **Replace** `uv run ty check src tests` → `uv check` in README, CI, and developer workflows
4. **Update Dockerfile** to support `uv check` in container CI
5. **Add pre-commit hook** for automated type safety on every commit
6. **Update `uv.lock`** to capture the lockfile-pinned ty binary version
7. **Update wiki/README** to document the unified quality gate

---

## References

- [Bringing uv and ty together](https://astral.sh/blog/uv-ty-integration) — Astral Blog (2026)
- [uv check CLI Reference](https://docs.astral.sh/uv/reference/cli/#uv-check) — Astral Docs
- [ty Configuration Reference](https://docs.astral.sh/ty/reference/configuration/) — Astral Docs
- [ty Pre-commit Hook](https://github.com/astral-sh/ty-pre-commit) — GitHub
- [[../specs/RFC-013_Static_Type_Safety_With_Ty]] — BAMF Dominator RFC-013

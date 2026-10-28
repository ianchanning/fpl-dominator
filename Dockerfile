# ==============================================================================
# BAMF DOMINATOR - MULTI-STAGE HARVESTER & CHIMERA ENGINE (RFC-012)
# ==============================================================================
# Three-stage build with 4 independently-cached layer groups:
#   1. Playwright Chromium (cached until PLAYWRIGHT_VERSION arg changes)
#   2. Python dependencies (cached until uv.lock changes)
#   3. Verification gate (uv check — static type safety)
#   4. Source code (sub-second rebuild)
# ==============================================================================

FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/app/.venv

# `git` is baked in because the GH Actions container job inherits NOTHING from
# the host runner: checkout v7 silently falls back to a tarball without it
# (no .git dir -> the harvester's commit/push step cannot work), and the
# `git config --global --add safe.directory` step exits 127 (RUD 40661580420).
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    glpk-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# VIRTUAL_ENV pins every `uv pip` / `python` invocation inside the image to the
# baked /app/.venv regardless of CWD (steps run in /github/workspace, where no
# .venv exists). Without it, `uv pip install --no-deps -e .` aborts with
# "No virtual environment found" before it can re-link `fpl_dominator` to the
# freshly checked-out source.

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# ------------------------------------------------------------------------------
# Layer 1: Playwright Browsers (cached until PLAYWRIGHT_VERSION changes)
# Placed BEFORE lockfile COPY so uv.lock changes don't cascade here.
# Version MUST match uv.lock: grep 'name = "playwright"' uv.lock -A1
# ------------------------------------------------------------------------------
ARG PLAYWRIGHT_VERSION=1.64.0
RUN uvx --from=playwright==${PLAYWRIGHT_VERSION} playwright install --with-deps chromium && \
    chmod -R 755 /ms-playwright

# ------------------------------------------------------------------------------
# Layer 2: Python Dependencies (cached until pyproject.toml or uv.lock change)
# ------------------------------------------------------------------------------
COPY pyproject.toml uv.lock README.md ./

RUN uv venv /app/.venv && \
    uv sync --frozen --no-install-project

# ------------------------------------------------------------------------------
# Stage 2: Verification Gate (catches type regressions before container ships)
# ------------------------------------------------------------------------------
FROM builder AS verifier

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src/
COPY tests/ /app/tests/
RUN uv sync --frozen

# Static type safety gate — fails the build on any ty diagnostic
RUN uv check

# ------------------------------------------------------------------------------
# Stage 3: Runtime (sub-second rebuild on src/ changes)
# ------------------------------------------------------------------------------
FROM builder AS runner

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src/
RUN uv sync --frozen

ENTRYPOINT ["bamf"]
CMD ["--help"]

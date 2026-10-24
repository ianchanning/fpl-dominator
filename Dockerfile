# ==============================================================================
# BAMF DOMINATOR - MULTI-STAGE HARVESTER & CHIMERA ENGINE (RFC-012)
# ==============================================================================
# Two-stage build with 3 independently-cached layer groups:
#   1. Playwright Chromium (cached until PLAYWRIGHT_VERSION arg changes)
#   2. Python dependencies (cached until uv.lock changes)
#   3. Source code (sub-second rebuild)
# ==============================================================================

FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    glpk-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

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
# Stage 2: Runtime (sub-second rebuild on src/ changes)
# ------------------------------------------------------------------------------
FROM builder AS runner

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src/
RUN uv sync --frozen

ENTRYPOINT ["bamf"]
CMD ["--help"]

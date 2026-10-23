# ==============================================================================
# BAMF DOMINATOR - AUTONOMOUS HARVESTER & CHIMERA ENGINE RUNNER (RFC-012)
# ==============================================================================
# Multi-purpose image for high-speed local development and GitHub Actions CI runner.
# Pre-bakes GLPK solver (glpsol), Astral uv, Playwright Chromium, and system fonts.
# ==============================================================================

FROM python:3.12-slim-bookworm

# Anti-Gambit Environment Tuning
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Install system dependencies: glpk-utils for Chimera MILP solver, git, curl, ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    glpk-utils \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv binary from official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency specifications for layer caching
COPY pyproject.toml uv.lock ./

# Create virtual environment, install dependencies, and bake Playwright Chromium + OS deps
RUN uv venv /app/.venv && \
    uv sync --frozen --no-install-project && \
    uv run playwright install --with-deps chromium && \
    chmod -R 777 /ms-playwright

# Copy source code and grimoire
COPY src/ /app/src/
COPY README.md /app/README.md

# Install project package into virtualenv
RUN uv sync --frozen

# Entrypoint default for CLI invocations
ENTRYPOINT ["bamf"]
CMD ["--help"]

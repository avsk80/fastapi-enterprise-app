# ---------- Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Get uv binary (fast + recommended)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install deps into /app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code
COPY app ./app

# ---------- Runtime ----------
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd -m appuser
USER appuser

# Copy venv + app
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/app /app/app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Dockerfile (at repo root)
FROM python:3.12-slim

WORKDIR /app

# Install uv + deps
RUN pip install --no-cache-dir uv

# Copy project files
# COPY pyproject.toml uv.lock ./
# RUN uv sync --frozen --no-cache

# only copy project metadata first for better layer caching
COPY pyproject.toml ./
# (do NOT COPY uv.lock here)

# resolve and install dependencies (no dev)
RUN uv pip install --system --no-cache -r <(uv pip compile -q pyproject.toml)

COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
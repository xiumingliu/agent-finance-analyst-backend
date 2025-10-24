FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir uv

# copy just metadata first for better caching
COPY pyproject.toml ./
# install deps into the system interpreter
RUN uv sync --no-dev --system

# now the app code
COPY app ./app

ENV HOST=0.0.0.0 PORT=8000
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host","0.0.0.0","--port","8000"]
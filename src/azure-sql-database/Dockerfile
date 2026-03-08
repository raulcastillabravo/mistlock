FROM python:3.12-slim

WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy dependencies first for caching
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# Copy application files
COPY main.py .

# Standardize binary path
ENV PATH="/app/.venv/bin:$PATH"

# Run FastAPI app
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]

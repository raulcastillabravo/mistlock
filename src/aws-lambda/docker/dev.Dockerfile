FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Upgrade pip and install uv
RUN pip3 install --upgrade pip && pip3 install uv

# Set working directory
WORKDIR /workspaces/aws-lambda

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN uv sync

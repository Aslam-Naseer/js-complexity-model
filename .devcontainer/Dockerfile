FROM mcr.microsoft.com/devcontainers/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

USER vscode
ENV UV_LINK_MODE=copy

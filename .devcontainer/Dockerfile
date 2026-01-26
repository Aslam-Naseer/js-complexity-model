FROM mcr.microsoft.com/devcontainers/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

USER vscode
ENV UV_LINK_MODE=copy

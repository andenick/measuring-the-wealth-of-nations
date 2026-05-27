# RMWND — Measuring the Wealth of Nations Replication
# Reproducible build environment for the Anu Framework v12.0 pipeline.
#
# Build:  docker build -t rmwnd:v1.1 -f Technical/Dockerfile Technical
# Run:    docker run --rm rmwnd:v1.1 status
# Shell:  docker run --rm -it --entrypoint /bin/bash rmwnd:v1.1
#
# Python target: 3.13 (slim); see requirements.txt for pinned deps.

FROM python:3.13-slim AS base

LABEL org.opencontainers.image.title="RMWND"
LABEL org.opencontainers.image.description="Measuring the Wealth of Nations (Shaikh & Tonak 1994) replication — Anu v12.0"
LABEL org.opencontainers.image.version="1.1"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- system deps (git for provenance; build-essential for numpy/scipy wheels fallback) ----
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- python deps: copy requirements first so layer caches across code changes ----
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# ---- project artifacts (read-only at build time) ----
COPY build.py            /app/build.py
COPY series_registry.json /app/series_registry.json
COPY PIPELINE_STATE.json  /app/PIPELINE_STATE.json
COPY ANU_LEDGER.json      /app/ANU_LEDGER.json
COPY code/                /app/code/
COPY data/                /app/data/
COPY viz/                 /app/viz/
COPY tools/               /app/tools/
COPY scripts/             /app/scripts/
COPY docs/                /app/docs/
COPY research/            /app/research/
COPY chopped/             /app/chopped/
COPY extenbooks/          /app/extenbooks/
COPY Build/               /app/Build/

# Make build.py the default callable; subcommands are positional args.
ENTRYPOINT ["python", "/app/build.py"]
CMD ["status"]

# Liveness: `build.py status` is a read-only pipeline-state probe.
HEALTHCHECK --interval=60s --timeout=15s --start-period=10s --retries=2 \
    CMD python /app/build.py status >/dev/null 2>&1 || exit 1

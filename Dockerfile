# RMWND — Measuring the Wealth of Nations Replication
# Reproducible build environment for the Anu Framework v12.0 pipeline.
#
# Build:  docker build -t rmwnd:2.0.0 -f Dockerfile .
# Run:    docker run --rm rmwnd:2.0.0 status
# Shell:  docker run --rm -it --entrypoint /bin/bash rmwnd:2.0.0
#
# Python target: 3.13 (slim); see requirements.txt for pinned deps.

FROM python:3.13-slim AS base

LABEL org.opencontainers.image.title="RMWND"
LABEL org.opencontainers.image.description="Measuring the Wealth of Nations (Shaikh & Tonak 1994) replication — Anu v12.0"
LABEL org.opencontainers.image.version="2.0.0"
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
# Only the shipped, tracked bundle paths are copied (see .publish_ignore / the
# repository tree). build.py reads series_registry.json + PIPELINE_STATE.json;
# the numbered pipeline, data, docs, viz, extenbooks, and tests round out the tree.
COPY build.py            /app/build.py
COPY series_registry.json /app/series_registry.json
COPY PIPELINE_STATE.json  /app/PIPELINE_STATE.json
COPY code/                /app/code/
COPY data/                /app/data/
COPY viz/                 /app/viz/
COPY docs/                /app/docs/
COPY extenbooks/          /app/extenbooks/
COPY tests/               /app/tests/

# Make build.py the default callable; subcommands are positional args.
ENTRYPOINT ["python", "/app/build.py"]
CMD ["status"]

# Liveness: `build.py status` is a read-only pipeline-state probe.
HEALTHCHECK --interval=60s --timeout=15s --start-period=10s --retries=2 \
    CMD python /app/build.py status >/dev/null 2>&1 || exit 1

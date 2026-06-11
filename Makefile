# RMWND — Measuring the Wealth of Nations Replication
# Convenience targets wrapping build.py + anu-doctor + Docker.
#
# Usage: make <target>
# Run `make help` for the target catalogue.
#
# This Makefile is GNU-make-flavoured. On Windows, install via Chocolatey
# (`choco install make`), MSYS2, or use WSL.

PYTHON      ?= python
PIP         ?= pip
PYTEST      ?= $(PYTHON) -m pytest
BUILD       := $(PYTHON) build.py
# project doctor runs in the maintainer workspace, not in this repo
DOCKER      ?= docker
IMAGE       ?= rmwnd:v1.1
PROJECT_DIR := .
TESTS_DIR   ?= tests

.PHONY: help install build test doctor review viz clean docker-build docker-run \
        chopped extenbooks ledger status all

help:
	@echo "RMWND Makefile targets:"
	@echo "  install        pip install -r requirements.txt"
	@echo "  build          regenerate chopped + extenbooks + ledger (full pipeline tail)"
	@echo "  chopped        regenerate Anu Chopped CSVs only"
	@echo "  extenbooks     regenerate Anu Extenbook workbooks only"
	@echo "  ledger         regenerate ANU_LEDGER.json only"
	@echo "  status         print PIPELINE_STATE stage table"
	@echo "  test           run pytest under $(TESTS_DIR)/"
	@echo "  doctor         (maintainer-only; anu-doctor is not shipped in this repo)"
	@echo "  review         summarise the latest build review output"
	@echo "  viz            run viz quality checker"
	@echo "  clean          remove scratch and v1.1 patch artifacts (destructive!)"
	@echo "  docker-build   build the rmwnd:v1.1 image"
	@echo "  docker-run     run the rmwnd:v1.1 image (default cmd: status)"
	@echo "  all            install + build + test"

install:
	$(PIP) install -r requirements.txt

build: chopped extenbooks ledger

chopped:
	$(BUILD) chopped

extenbooks:
	$(BUILD) extenbooks

ledger:
	$(BUILD) ledger

status:
	$(BUILD) status

test:
	$(PYTEST) $(TESTS_DIR)/

doctor:
	@echo "anu-doctor (project mode) runs in the maintainer workspace, not in this repo"

review:
	$(BUILD) review

viz:
	$(BUILD) viz

# Destructive: scratch + v1.1 stage patches. Will not touch registry / pipeline state.
clean:
	@echo "Removing scratch + v1.1 patch artifacts (registry/pipeline/ledger preserved)"
	-rm -rf data/scratch/*
	-rm -rf _v1.1_patches/*
	-rm -rf _stage3_patches/*
	-rm -rf _stage5_patches/*
	-find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	-find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +

docker-build:
	$(DOCKER) build -t $(IMAGE) -f Dockerfile .

docker-run:
	$(DOCKER) run --rm $(IMAGE) status

all: install build test

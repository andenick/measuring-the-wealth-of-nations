# RMWND Pre-Commit Check

**Version**: 1.0
**Authored**: 2026-05-23 (v1.1 Phase 2)
**Script**: `Technical/code/utils/precommit_check.py`
**Installer**: `Technical/code/utils/install_precommit_hook.sh`

Mechanical enforcement of the eight binding Anu-Framework / RMWND Decisions
(0001–0008) on every commit. The script is read-only with respect to
`series_registry.json`, `PIPELINE_STATE.json`, `ANU_BUILD_MANIFEST.json`,
`ANU_LEDGER.json`, and `SUBSERIES_PLAN.json`.

## Quick usage

```bash
# Whole-project audit (the project has no .git repo; this is the default)
python Technical/code/utils/precommit_check.py --all

# Show PASS lines too (default suppresses them)
python Technical/code/utils/precommit_check.py --all -v

# Ad-hoc glob (patterns are relative to the project root)
python Technical/code/utils/precommit_check.py --files "Technical/chopped/*.csv"

# Git pre-commit context (use only if a .git repo exists)
python Technical/code/utils/precommit_check.py --staged
```

Exit code: **0** on all-PASS / WARN, **1** on any FAIL.

## Installation as a git pre-commit hook

The RMWND project's nested `.git` repositories were stripped during the
v0.4 hyper-review honesty pass. The installer is included for completeness
and for downstream forks that maintain their own git history:

```bash
bash Technical/code/utils/install_precommit_hook.sh
```

If no `.git/` directory is found, the installer prints the manual-invocation
form and exits 0 without writing anything.

## The eight checks

| Decision | Scope                                | Check                                                                            | Level on violation |
|----------|--------------------------------------|----------------------------------------------------------------------------------|--------------------|
| 0001     | `Technical/extenbooks/*.xlsx`        | Sheet names == `['Data','Provenance','Research','Construction']` (or +'Validation') | FAIL               |
| 0002     | `Technical/series_registry.json`     | Every series carries non-empty `validation.reference_values` (or `derived_statistics` per 0008) | FAIL               |
| 0003     | `Technical/series_registry.json`     | `extension=null` ⇒ status ≠ `validated_book_and_extension`                       | FAIL               |
| 0003     | `Technical/series_registry.json`     | `extension≠null` ⇒ status contains `extension`                                   | WARN¹              |
| 0004     | `Technical/code/{L01,P02,V03,M04,A05,O06,S00}_*.py` | Filename matches `<phase>_<SID>[_<suffix>].py`                            | FAIL               |
| 0005     | `Technical/chopped/*.csv`            | Row 1 has `#`-prefixed metadata, row 2 starts with `Year`, row 3 starts with 4-digit year | FAIL               |
| 0006     | (meta)                               | Always PASS — code-is-source-of-truth is enforced by `anu-doctor` + human review | n/a (informational) |
| 0007     | `Technical/research/*_research.json` | ≥3 canonical entries with `entry_type=='verbatim_quote'`, `source_ref`, and (content or verbatim_quote) populated | FAIL               |
| 0008     | `Technical/series_registry.json`     | Every `reference_values` key parses as int year; every value is a finite scalar  | FAIL               |

¹ Per project CLAUDE.md, populating the `extension` block is allowed before the
extension stage has actually run; the status upgrade to
`validated_book_and_extension` only follows successful extension + validation.
The check therefore WARNs rather than FAILs on this branch so that planning-stage
registry edits aren't blocked.

## File-discovery modes

- **`--all`** — explicit whole-project scan (extenbooks, chopped CSVs, research
  JSONs, phase scripts under `Technical/code/`, and the registry).
- **`--staged`** — files appearing in `git diff --cached --name-only`.
- **`--files <glob> [<glob> ...]`** — ad-hoc patterns, relative to project root.
- **No flag** — auto: `--staged` if a `.git` repo is detected, otherwise `--all`.

The Decision-0002 / 0003 / 0008 checks always run when the registry is
reachable, regardless of whether it was in the file list. This guarantees the
hook never silently "passes" because a non-registry edit happened to be the
only staged change.

## Disabling / bypassing

- **Single-commit bypass**: `git commit --no-verify` (discouraged; investigate
  the failure first).
- **Permanent disable**: delete `.git/hooks/pre-commit` (or rename it).
- **Manual audits**: never blocked by the hook — they only run when you
  invoke the script directly.

## When a check fails

1. Read the FAIL line; each one names the file and the specific contract
   violation.
2. Per the project rules (`(local path)` —
   *No Synthetic Data*), do **not** "fix" a FAIL by inventing values to
   satisfy a contract. Either supply real data or downgrade the series'
   status and remove the offending field.
3. The script is read-only by design; it will never auto-rewrite the
   registry / chopped CSVs / extenbooks to make a check pass.

## Adding a check

Follow the existing pattern in `precommit_check.py`:

```python
def check_decision_XXXX(files: Iterable[Path], rpt: Report) -> None:
    ...
    rpt.add("Decision-XXXX", "PASS"|"WARN"|"FAIL", path_str, message)

ALL_CHECKS.append(("Decision-XXXX", check_decision_XXXX))
```

…then document the check in the table above and update the corresponding
Decision document under `(internal)/docs/decisions/` (the canonical
location for all framework + project-scoped decisions; see
`(internal)/docs/decisions/README.md`).

## References

- `(internal)/docs/decisions/0007_verbatim_quote_schema.md`
- `(internal)/docs/decisions/0008_reference_values_year_keyed_scalars.md` (moved from `Technical/docs/decisions/` to canonical Council location in v1.2 iter2)
- `(local path)`
- `(local path)` (project-specific anti-patterns)

# GitHub Release Guide — RMWND v1.2

**Status**: Manual execution required. Repository creation and `git push` need authenticated user credentials (SSH key, GitHub PAT, or `gh auth login`); CI/agent automation must not push as the user without explicit approval.

**Estimated time**: 20–30 minutes (longer if minting a new SSH key or PAT).

---

## Goal

Publish the `Outputs/Publish/` bundle as the public GitHub repo for RMWND v1.2, cut the `v1.2` tag, and create a GitHub Release with the bundle zip attached.

---

## Prerequisites

1. `git` configured locally with `user.name` and `user.email` (the maintainer runs these; automation must never touch git config).
2. Authentication of choice:
   - SSH key registered on GitHub (`ssh -T git@github.com` returns "successfully authenticated"), OR
   - GitHub CLI (`gh auth login`), OR
   - HTTPS + Personal Access Token in the credential helper.
3. The CI workflow (`.github/workflows/ci.yml`) is already present at the project root.
4. `Outputs/Publish/` is fully populated (verified at scaffold time).

---

## Step 1 — Initialize the publish repo

```powershell
# Run from the root of this publish bundle.
Set-Location <path-to-this-repo>

# Sanity: make sure nothing here was previously initialised.
if (Test-Path .git) { throw ".git already exists — handle manually before re-init." }

git init -b main
git add .
git status              # confirm scope
git commit -m "RMWND v1.2 release"
```

Note: a `.gitignore` should already exclude transient artifacts (`__pycache__/`, `.DS_Store`, etc.). If it does not, add one before the first commit — the publish bundle is meant to ship clean.

---

## Step 2 — Create the GitHub repo

### Option A — `gh` CLI (recommended)

```powershell
# Private first; flip to public when v1.2 is announced.
gh repo create <OWNER>/rmwnd `
  --private `
  --description "Replication and extension of Shaikh & Tonak (1994) Measuring the Wealth of Nations" `
  --source . `
  --remote origin `
  --push
```

This creates the repo, registers `origin`, and pushes `main` in one step.

### Option B — manual

1. Visit https://github.com/new and create `<OWNER>/rmwnd` (Private, no README/.gitignore/license — the local commit already has them).
2. Wire up the remote and push:

   ```powershell
   git remote add origin git@github.com:<OWNER>/rmwnd.git
   git push -u origin main
   ```

---

## Step 3 — Verify CI ran

After the first push, GitHub Actions should pick up `.github/workflows/ci.yml` and run the `test` job across Python 3.11 / 3.12 / 3.13.

```powershell
gh run list --workflow ci.yml --limit 5
gh run watch                          # streams the latest run
```

Diagnose failures before tagging. The CI badge in `README.md` (placeholder `OWNER/REPO`) should be updated to the real owner/repo path once the first successful run is recorded:

```powershell
# In README.md and Outputs/Publish/README.md replace:
#   https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg
# with:
#   https://github.com/<your-owner>/rmwnd/actions/workflows/ci.yml/badge.svg
```

Commit the badge fix and push.

---

## Step 4 — Tag the release

```powershell
git tag -a v1.2 -m "RMWND v1.2 release — S513 stock-form + EXEMPLARY anu-review"
git push --tags
```

Verify the tag landed:

```powershell
gh release list
git ls-remote --tags origin
```

---

## Step 5 — Create the GitHub Release

```powershell
$body = @"
RMWND v1.2 — academic-grade public-ready release.

## Highlights
- Chapter 7 series (S701/S702/S703) carry `proxy: false`
- S513/S514 stock-form primary per DIV-012
- anu-review: 97.59 EXEMPLARY (D13 + D14 cleared)
- 90 PASS pytest + 1 honest XFAIL on S505 wedge

## Provenance
- 64 series, 1925–2024
- 12 entries in DIVERGENCE_REGISTER
- Built on Anu Framework v12.1

Full notes in CHANGELOG.md.
"@

gh release create v1.2 `
  "<path-to-release-archive>\RMWND_v1.2_release.zip" `
  --title "RMWND v1.2" `
  --notes $body
```

---

## Step 6 — Flip to public

When ready to announce:

```powershell
gh repo edit <OWNER>/rmwnd --visibility public --accept-visibility-change-consequences
```

Sanity-check:

```powershell
gh repo view <OWNER>/rmwnd --json visibility
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied (publickey)` | SSH key not registered on GitHub | `gh ssh-key add ~/.ssh/id_ed25519.pub` |
| `remote: Repository not found` | Wrong `<OWNER>` or repo still private and you lack access | Re-create with correct owner or accept the invite |
| CI workflow does not run | `.github/workflows/ci.yml` missing from the initial commit | Re-verify `git ls-files .github/workflows/ci.yml`, recommit, push |
| `gh release create` fails on artifact path | Path with spaces or zip missing | Quote the path; verify `Test-Path "<path-to-release-archive>\RMWND_v1.2_release.zip"` |
| Badge still 404s | Wrong owner/repo in markdown | Search-replace `OWNER/REPO` everywhere it appears |

---

## After release

- GitHub repo public: ☐
- `v1.2` tag pushed: ☐
- CI green on `main` and on the tag: ☐
- GitHub Release created with zip attached: ☐

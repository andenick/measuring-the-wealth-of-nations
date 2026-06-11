# Verifying RMWND v1.2 Release Signatures

**Status (2026-05-24T06:38:45Z)**: BLOCKED — no GPG signing key available on the build host.

## Why this file exists

Per the v1.2 release plan, the release archive bundle should be GPG-signed (detached `.asc` signatures on the zipped archive and on `MANIFEST.json`) so downstream consumers can verify provenance.

## Current state

- `gpg --version`: GnuPG 2.4.7 installed
- `gpg --list-secret-keys`: empty (no secret key present)
- No detached signatures produced yet

## What the user must do before signing can proceed

1. Generate a long-lived signing key:
   ```
   gpg --full-generate-key
   ```
   Recommended: RSA 4096, no expiry (or 5+ years), passphrase-protected, identity = the project maintainer's name + email.

2. Note the resulting key ID:
   ```
   gpg --list-secret-keys --keyid-format=long
   ```

3. Export the public key to the publish package:
   ```
   gpg --armor --export <KEY_ID> > PUBLIC_KEY.asc
   ```

## What a future signing iteration will run

```powershell
# 1. Zip the release directory (if not already zipped)
Compress-Archive -Path ./* `
                 -DestinationPath RMWND_v1.2_release.zip

# 2. Sign the zip
gpg --detach-sign --armor RMWND_v1.2_release.zip
# produces RMWND_v1.2_release.zip.asc

# 3. Sign the manifest (so it can be verified independently of the zip)
gpg --detach-sign --armor MANIFEST.json
# produces MANIFEST.json.asc

# 4. The signatures + public key sit alongside the release files
#    (RMWND_v1.2_release.zip.asc, MANIFEST.json.asc, PUBLIC_KEY.asc)
```

## How a downstream consumer verifies (after signatures are produced)

```
# Import the project's public key
gpg --import PUBLIC_KEY.asc

# Verify the zipped archive
gpg --verify RMWND_v1.2_release.zip.asc RMWND_v1.2_release.zip

# Verify the manifest
gpg --verify MANIFEST.json.asc MANIFEST.json
```

Both commands should report `Good signature from "<maintainer identity>"`. If either reports `BAD signature` or `Can't check signature: No public key`, the archive has been tampered with or the wrong key is being used.

## Iteration blocker summary

- **Cause**: no GPG secret key on host
- **Owner**: human user (key generation requires interactive passphrase entry; not safely automatable from an agent session)
- **Unblocks**: v1.2 plan C.3 closure
- **Workaround until then**: SHA-256 checksums in `MANIFEST.json` provide tamper-evidence (just not non-repudiation)

---

**Logged in STEP_LOG**: step_id `v1.2-iter6-D4-C3-appendixF-gpg`, outcome `partial` (Appendix F validated, GPG blocked on missing key).

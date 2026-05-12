#!/usr/bin/env python3
"""Fetch Turkish Ministry of Finance budget data using Playwright."""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "data" / "raw-data" / "turkey_muhasebat"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("https://muhasebat.hmb.gov.tr/1994-2005-butce-istatistikleri", "1994-2005"),
    ("https://muhasebat.hmb.gov.tr/merkezi-yonetim-butce-istatistikleri", "merkezi-yonetim"),
    ("https://muhasebat.hmb.gov.tr/genel-yonetim-butce-istatistikleri", "genel-yonetim"),
    ("https://muhasebat.hmb.gov.tr/genel-yonetim-mali-istatistikleri", "mali-istatistikleri"),
]


def fetch_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)

        for url, label in PAGES:
            print(f"\n{'='*60}")
            print(f"Browsing: {url}")
            page = context.new_page()

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                content = page.content()
                html_path = OUT_DIR / f"{label}_page.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  Saved HTML: {html_path.name}")

                links = page.eval_on_selector_all(
                    "a[href]",
                    """els => els.map(el => ({
                        href: el.href,
                        text: el.textContent.trim().substring(0, 80)
                    }))"""
                )

                download_links = []
                for link in links:
                    href = link.get("href", "")
                    if any(ext in href.lower() for ext in [".xls", ".xlsx", ".csv", ".pdf"]):
                        download_links.append(link)

                print(f"  Found {len(download_links)} downloadable files")

                for dl in download_links:
                    href = dl["href"]
                    text = dl["text"][:50]
                    fname = href.split("/")[-1].split("?")[0]
                    if not fname:
                        continue

                    from urllib.parse import unquote
                    fname = unquote(fname)
                    out_path = OUT_DIR / f"{label}_{fname}"

                    if out_path.exists():
                        print(f"  SKIP (exists): {out_path.name}")
                        continue

                    print(f"  Downloading: {fname} ({text})")
                    try:
                        with page.expect_download(timeout=15000) as dl_info:
                            page.evaluate(f"window.open('{href}')")
                        download = dl_info.value
                        download.save_as(str(out_path))
                        size = out_path.stat().st_size
                        print(f"    Saved: {out_path.name} ({size/1024:.1f}KB)")
                    except Exception as e:
                        try:
                            import urllib.request
                            urllib.request.urlretrieve(href, str(out_path))
                            size = out_path.stat().st_size
                            print(f"    Saved (urllib): {out_path.name} ({size/1024:.1f}KB)")
                        except Exception as e2:
                            print(f"    FAILED: {e2}")

            except Exception as e:
                print(f"  ERROR: {e}")
            finally:
                page.close()

        browser.close()

    files = list(OUT_DIR.glob("*"))
    print(f"\n{'='*60}")
    print(f"Total files in {OUT_DIR}: {len(files)}")
    for f in sorted(files):
        print(f"  {f.name} ({f.stat().st_size/1024:.1f}KB)")


if __name__ == "__main__":
    fetch_all()

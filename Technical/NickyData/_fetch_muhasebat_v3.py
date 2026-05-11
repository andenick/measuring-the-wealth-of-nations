#!/usr/bin/env python3
"""Click into muhasebat sub-pages and find actual download links."""

import json
import re
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("D:/Arcanum/Projects/ST2/Inputs/ExternalSources/Turkey2022/muhasebat")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SUB_PAGES = [
    "https://muhasebat.hmb.gov.tr/1924-1989-yillari-yillik-bazli-konsolide-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/1924-2005-ozet-tablolar",
    "https://muhasebat.hmb.gov.tr/1990-2003-yillari-yillik-bazli-konsolide-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/1994-2002-yillari-konsolide-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/2003-2005-yillari-konsolide-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/genel-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/2011-2024-genel-yonetim-butce-istatistikleri",
]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        for url in SUB_PAGES:
            label = url.split("/")[-1][:40]
            print(f"\n{'='*60}")
            print(f"Sub-page: {label}")

            page = context.new_page()
            all_urls = []

            def capture(response):
                u = response.url
                if response.ok:
                    ct = response.headers.get("content-type", "")
                    if "json" in ct:
                        try:
                            body = response.text()
                            found = re.findall(r'https?://[^"\s\\]+\.(?:xlsx|xls|csv)', body)
                            all_urls.extend(found)
                        except Exception:
                            pass

            page.on("response", capture)

            try:
                page.goto(url, wait_until="networkidle", timeout=20000)
                time.sleep(2)

                text = page.inner_text("body")
                lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 3]

                # Also check rendered HTML for download links
                html = page.content()
                html_urls = re.findall(r'href="(https?://[^"]+\.(?:xlsx|xls|csv))"', html)
                all_urls.extend(html_urls)

                # Check for ms.hmb.gov.tr upload links in HTML
                ms_urls = re.findall(r'(https?://ms\.hmb\.gov\.tr/uploads/[^"\\]+\.(?:xlsx|xls|pdf))', html)
                all_urls.extend(ms_urls)

                unique = list(set(all_urls))
                print(f"  Content lines: {len(lines)}")
                print(f"  Download URLs found: {len(unique)}")

                for u in unique:
                    fname = u.split("/")[-1].split("?")[0]
                    from urllib.parse import unquote
                    fname = unquote(fname)
                    safe_fname = f"{label}_{fname}"[:100]
                    out_path = OUT_DIR / safe_fname

                    if out_path.exists():
                        print(f"  SKIP: {safe_fname}")
                        continue

                    print(f"  Downloading: {fname[:60]}")
                    try:
                        urllib.request.urlretrieve(u, str(out_path))
                        size = out_path.stat().st_size
                        if size < 1000:
                            out_path.unlink()
                            print(f"    Too small ({size}B), deleted")
                        else:
                            print(f"    OK: {size/1024:.1f}KB")
                    except Exception as e:
                        print(f"    FAIL: {e}")

                if not unique:
                    # Print page content to understand structure
                    for line in lines[:15]:
                        print(f"    {line[:80]}")

            except Exception as e:
                print(f"  ERROR: {e}")
            finally:
                page.close()

        browser.close()

    # Final inventory
    print(f"\n{'='*60}")
    print("Files downloaded:")
    for f in sorted(OUT_DIR.glob("*")):
        if f.suffix not in ['.html', '.txt']:
            print(f"  {f.name} ({f.stat().st_size/1024:.1f}KB)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch Turkish Ministry of Finance budget data - intercept XHR and extract rendered content."""

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("D:/Arcanum/Projects/ST2/Inputs/ExternalSources/Turkey2022/muhasebat")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    "https://muhasebat.hmb.gov.tr/1994-2005-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/merkezi-yonetim-butce-istatistikleri",
    "https://muhasebat.hmb.gov.tr/genel-yonetim-butce-istatistikleri",
]

captured_requests = []


def on_response(response):
    url = response.url
    if any(kw in url.lower() for kw in ["api", "data", "json", "excel", "xls", "csv", "butce", "istatistik", "dosya"]):
        try:
            ct = response.headers.get("content-type", "")
            size = len(response.body()) if response.ok else 0
            captured_requests.append({
                "url": url[:200],
                "status": response.status,
                "content_type": ct[:60],
                "size": size,
            })
        except Exception:
            pass


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        for url in PAGES:
            label = url.split("/")[-1]
            print(f"\n{'='*60}")
            print(f"Page: {label}")

            page = context.new_page()
            page.on("response", on_response)
            captured_requests.clear()

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(3)

                # Try scrolling to trigger lazy-loaded content
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)

                # Get all text content
                text = page.inner_text("body")
                text_path = OUT_DIR / f"{label}_text.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text)
                lines = text.strip().split("\n")
                print(f"  Page text: {len(lines)} lines, {len(text)} chars")

                # Print first 30 lines to see what content is there
                for line in lines[:30]:
                    line = line.strip()
                    if line and len(line) > 3:
                        print(f"    {line[:100]}")

                # Look for any clickable elements that might trigger downloads
                buttons = page.query_selector_all("button, .btn, [role='button'], a.download, .download-btn, .excel-btn")
                print(f"  Buttons/download elements: {len(buttons)}")

                # Check for accordion/tab content
                accordions = page.query_selector_all(".accordion, .tab-content, .panel, .collapse, .expandable")
                print(f"  Accordion/tab elements: {len(accordions)}")

                # Check captured XHR
                if captured_requests:
                    print(f"  Captured API calls: {len(captured_requests)}")
                    for req in captured_requests:
                        print(f"    {req['status']} {req['content_type'][:30]} {req['size']}B {req['url'][:80]}")
                else:
                    print("  No API calls captured")

            except Exception as e:
                print(f"  ERROR: {e}")
            finally:
                page.close()

        browser.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Capture main-flow phone screenshots for PRD (demo.html?flow=&capture=1)."""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo.html"
OUT = ROOT / "assets" / "prd-shots"

FLOWS = [
    "list-active",
    "list-shelved",
    "detail-active",
    "detail-shelved",
    "create-step1",
    "create-step2",
    "create-step3",
    "create-success",
    "issue-success",
    "pick-projects",
    "pick-discount-list",
]


def main() -> int:
    if not DEMO.is_file():
        print(f"Missing {DEMO}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    demo_url = DEMO.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 420, "height": 900}, device_scale_factor=2)
        for flow in FLOWS:
            url = f"{demo_url}?flow={flow}&capture=1"
            print(f"Capture {flow} …")
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(700)
            phone = page.locator(".phone").first
            phone.wait_for(state="visible")
            out = OUT / f"{flow}.png"
            phone.screenshot(path=str(out), type="png")
            print(f"  → {out.name} ({out.stat().st_size} bytes)")
        browser.close()
    print(f"Done. {len(FLOWS)} shots in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

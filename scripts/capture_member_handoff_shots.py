# -*- coding: utf-8 -*-
"""Capture membership-card FLOW_NAV screens into native-handoff-member-card/captures."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo.html"
OUT = ROOT / "native-handoff-member-card" / "captures"

FLOWS = [
    "list-active",
    "list-shelved",
    "card-groups",
    "card-group-members",
    "card-group-create",
    "card-item-group",
    "detail-active",
    "detail-shelved",
    "create-step1",
    "create-step2",
    "create-step3",
    "create-success",
    "issue-success",
    "pick-projects",
    "pick-products",
    "pick-discount-list",
    "card-issue-new",
    "card-quick-issue",
    "card-issue-holders",
    "card-extend",
    "card-refund",
    "card-shelf",
    "card-reshelf",
    "card-stats-help",
    "card-unlimited-validity",
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    uri = DEMO.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 420, "height": 900}, device_scale_factor=2)
        for flow in FLOWS:
            url = f"{uri}?flow={flow}&capture=1"
            print(f"Capture {flow}")
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(900)
            phone = page.locator(".phone").first
            phone.wait_for(state="visible")
            out = OUT / f"{flow}.png"
            phone.screenshot(path=str(out), type="png")
            print(f"  -> {out.name} ({out.stat().st_size})")
        browser.close()
    print(f"Done {len(FLOWS)} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

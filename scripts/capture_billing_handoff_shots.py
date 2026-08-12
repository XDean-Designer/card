# -*- coding: utf-8 -*-
"""Capture 开单记账 FLOW_NAV screens into native-handoff-billing/captures."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo.html"
OUT = ROOT / "native-handoff-billing" / "captures"

FLOWS = [
    "bill-pick",
    "bill-bill",
    "bill-detail",
    "bill-cart",
    "bill-checkout",
    "bill-pay",
    "bill-pay-price-changed",
    "bill-success",
    "bill-scan-me",
    "bill-scan-cust",
    "bill-expand",
    "bill-add-card",
    "bill-add-card-group",
    "bill-card-asset",
    "bill-benefit",
    "bill-discount",
    "bill-hold",
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
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # bill-* handlers register after card boot; BillingDemo is last.
                page.wait_for_function(
                    "() => !!(window.BillingDemo && typeof window.applyFlowDeepLink === 'function')",
                    timeout=30000,
                )
                ok = page.evaluate(
                    """(fid) => {
                      if (typeof ensureDemoFilled === 'function') ensureDemoFilled();
                      document.documentElement.classList.add('prd-capture');
                      // Pre-seed cart + staff for settle/pay overlays so deep links can open
                      try {
                        if (window.BillingDemo) {
                          const needsCart = ['bill-detail','bill-cart','bill-checkout','bill-pay','bill-benefit','bill-discount'].includes(fid);
                          if (needsCart && typeof BillingDemo.ensureMember === 'function') BillingDemo.ensureMember();
                        }
                        const st = window.state || (window.BillingDemo && window.state);
                      } catch (e) {}
                      const applied = applyFlowDeepLink(fid);
                      // If checkout blocked by unset stations, force-open masks for capture
                      try {
                        if (fid === 'bill-checkout') {
                          const m = document.getElementById('checkoutMask');
                          if (m && !m.classList.contains('open')) {
                            if (typeof openMask === 'function') openMask('checkoutMask');
                            else m.classList.add('open');
                          }
                        }
                        if (fid === 'bill-pay') {
                          const m = document.getElementById('payMask');
                          if (m && !m.classList.contains('open')) {
                            if (typeof openBillPayMask === 'function') openBillPayMask();
                            else if (typeof openMask === 'function') openMask('payMask');
                            else m.classList.add('open');
                          }
                        }
                        if (fid === 'bill-cart') {
                          const m = document.getElementById('cartSheetMask');
                          if (m && !m.classList.contains('open')) {
                            if (typeof openMask === 'function') openMask('cartSheetMask');
                            else m.classList.add('open');
                          }
                        }
                      } catch (e2) {}
                      return applied;
                    }""",
                    flow,
                )
                if not ok:
                    print(f"  !! applyFlowDeepLink returned false for {flow}")
                page.wait_for_timeout(1400)
                phone = page.locator(".phone").first
                phone.wait_for(state="visible", timeout=15000)
                out = OUT / f"{flow}.png"
                phone.screenshot(path=str(out), type="png")
                print(f"  -> {out.name} ({out.stat().st_size})")
            except Exception as e:
                print(f"  !! FAIL {flow}: {e}")
        browser.close()
    sizes = sorted({(OUT / f"{f}.png").stat().st_size for f in FLOWS if (OUT / f"{f}.png").exists()})
    print(f"Done -> {OUT}; unique sizes={len(sizes)} {sizes[:8]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

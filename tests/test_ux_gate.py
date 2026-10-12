"""UX Quality Gate: repeatable visual evidence and interaction checks.

Run against the local HTTP server; reports never assert that screenshots were
human-reviewed. Automated heuristics are a minimum, not a UX certification.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/"
OUT = Path("test-artifacts")
OUT.mkdir(exist_ok=True)
checks = []
issues = []


def record(name, ok, detail=""):
    checks.append({"check": name, "passed": bool(ok), "detail": detail})
    if not ok:
        issues.append(name + (": " + detail if detail else ""))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    try:
        for label, width, height in [("desktop", 1440, 900), ("laptop", 1280, 800)]:
            page = browser.new_page(viewport={"width": width, "height": height})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            try:
                response = page.goto(URL, wait_until="networkidle")
                page.wait_for_selector(".node.page", timeout=10000)
                page.screenshot(path=str(OUT / ("ux-" + label + ".png")), full_page=True)
                record(label + ": HTTP response", response is not None and response.ok)
                record(label + ": JavaScript errors", not errors, "; ".join(errors))
                metrics = page.evaluate("""() => {
                  const viewport = document.documentElement.clientWidth;
                  const controls = [...document.querySelectorAll('button, input, select, textarea')];
                  const unnamed = controls.filter(el => {
                    if (el.disabled || el.getClientRects().length === 0) return false;
                    return !(el.getAttribute('aria-label') || el.getAttribute('title') ||
                      el.labels?.length || el.textContent?.trim() || el.getAttribute('placeholder'));
                  });
                  const badTargets = controls.filter(el => {
                    if (el.disabled || el.getClientRects().length === 0) return false;
                    const r = el.getBoundingClientRect();
                    return r.width < 20 || r.height < 20;
                  });
                  return {viewport, pageWidth: document.documentElement.scrollWidth,
                    unnamed: unnamed.map(el => el.outerHTML.slice(0,120)),
                    tinyControls: badTargets.map(el => el.outerHTML.slice(0,120))};
                }""")
                record(label + ": horizontal document overflow",
                       metrics["pageWidth"] <= metrics["viewport"] + 2,
                       json.dumps(metrics, ensure_ascii=False))
                record(label + ": control accessible names", not metrics["unnamed"],
                       json.dumps(metrics["unnamed"], ensure_ascii=False))
                # Minimum 20px heuristic, NOT a WCAG 2.2 AA certification.
                record(label + ": minimum control size", not metrics["tinyControls"],
                       json.dumps(metrics["tinyControls"], ensure_ascii=False))
            except Exception as exc:
                record(label + ": page inspection", False, str(exc))
                try:
                    page.screenshot(path=str(OUT / ("ux-" + label + "-failure.png")), full_page=True)
                except Exception:
                    pass
            finally:
                page.close()
    finally:
        browser.close()

report = {"gate": "UX09", "scope": "automated UX heuristics and screenshot capture",
          "human_visual_review": "not performed", "checks": checks,
          "passed": not issues, "failures": issues}
(OUT / "ux-gate.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
if issues:
    raise SystemExit(1)

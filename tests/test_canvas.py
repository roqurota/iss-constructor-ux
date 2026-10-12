from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_selector(".node.page")
    page.wait_for_timeout(250)
    assert not errors, f"JavaScript errors: {errors}"
    assert page.locator(".node.page").count() >= 2, "Pages did not render"
    assert page.locator(".mockbutton").count() >= 1, "Button did not render"

    # The button's own action should render above its parent Page,
    # not merely have the right mathematical starting point.
    result = page.evaluate("""() => {
      const btn = document.querySelector('.mockbutton[data-trigger]');
      const pageNode = btn.closest('.node.page');
      const svg = document.querySelector('.link-layer');
      const paths = [...document.querySelectorAll('#connectionPaths path[marker-end]')];
      const nav = paths.find(p => p.getAttribute('marker-end')?.includes('nav-arrow'));
      if (!nav) return {skip: 'No Navigate action in initial demo'};
      const b = btn.getBoundingClientRect();
      const p = nav.getPointAtLength(0);
      const pt = svg.createSVGPoint(); pt.x = p.x; pt.y = p.y;
      const start = pt.matrixTransform(svg.getScreenCTM());
      const above = document.elementFromPoint(start.x, start.y);
      return {withinButton: start.x >= b.left-3 && start.x <= b.right+3 &&
              start.y >= b.top-3 && start.y <= b.bottom+3,
              overlayAbovePage: svg.compareDocumentPosition(pageNode) & Node.DOCUMENT_POSITION_PRECEDING ? true : false,
              sourceVisible: above === svg || svg.contains(above),
              x:start.x, y:start.y, hit:above?.className?.baseVal || above?.className};
    }""")
    if "skip" not in result:
        assert result["withinButton"], f"Navigate arrow does not start at button: {result}"
        assert result["overlayAbovePage"], f"SVG is below Page in DOM: {result}"
    Path("test-artifacts").mkdir(exist_ok=True)
    page.screenshot(path="test-artifacts/canvas.png", full_page=True)
    browser.close()
print("Canvas smoke test passed")

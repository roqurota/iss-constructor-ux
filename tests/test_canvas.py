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

    # Create the action using the same controls a user uses.
    home = page.locator('.node.page').filter(has=page.locator('.nodehead', has_text='Home'))
    home.locator('.mockbutton').click()
    page.locator('#behaviorAction').select_option('navigate')
    page.locator('#behaviorTarget').click()
    page.locator('#targetOptions [data-target-id]', has_text='Gallery').click()
    page.locator('#applyBehavior').click()
    page.wait_for_selector('#connectionPaths path[marker-end*="nav-arrow"]')

    # UX09: multiple actions must coexist on one button, in order.
    home.locator('.mockbutton').click()
    page.locator('#behaviorAction').select_option('popup')
    page.locator('#behaviorTarget').click()
    page.locator('#targetOptions [data-target-id]', has_text='Info Popup').click()
    page.locator('#applyBehavior').click()
    page.locator('#behaviorAction').select_option('tcp')
    page.locator('#tcpCommand').fill('LIGHTS_ON')
    page.locator('#applyBehavior').click()
    assert page.locator('.multi-action').count() == 3, "Actions were overwritten instead of appended"
    assert page.locator('#connectionPaths path[marker-end*="nav-arrow"]').count() == 2, "Independent visual links missing"
    assert 'LIGHTS_ON' in page.locator('#actionList').inner_text(), "TCP action missing"
    page.locator('[data-action-up="2"]').click()
    assert page.locator('.multi-action').count() == 3, "Reorder dropped an action"
    page.locator('[data-action-remove="1"]').click()
    assert page.locator('.multi-action').count() == 2, "Remove should delete one action only"

    def inspect():
        return page.evaluate("""() => {
          const btn = [...document.querySelectorAll('.node.page')].find(n => n.querySelector('.nodehead')?.textContent.includes('Home'))?.querySelector('.mockbutton');
          const pageNode = btn.closest('.node.page');
          const svg = document.querySelector('.link-layer');
          const nav = document.querySelector('#connectionPaths path[marker-end*="nav-arrow"]');
          const b = btn.getBoundingClientRect();
          const startPoint = nav.getPointAtLength(0);
          const pt = svg.createSVGPoint(); pt.x = startPoint.x; pt.y = startPoint.y;
          const start = pt.matrixTransform(svg.getScreenCTM());
          const above = document.elementFromPoint(start.x, start.y);
          return {
            withinButton: start.x >= b.left-4 && start.x <= b.right+4 &&
              start.y >= b.top-4 && start.y <= b.bottom+4,
            overlayAfterPage: Boolean(svg.compareDocumentPosition(pageNode) & Node.DOCUMENT_POSITION_PRECEDING),
            overlayStacking: Number(getComputedStyle(svg).zIndex) > Number(getComputedStyle(pageNode).zIndex),
            start: {x: start.x, y: start.y}, button: {x:b.left,y:b.top,width:b.width,height:b.height},
            hit: above?.tagName
          };
        }""")

    result = inspect()
    print(f"Initial arrow geometry: {result}", flush=True)
    assert result['withinButton'], f"Navigate arrow starts outside button: {result}"
    assert result['overlayAfterPage'], f"SVG overlay is behind Page: {result}"
    assert result['overlayStacking'], f"Arrow overlay stacking is behind Page: {result}"

    # Move Home via the actual drag gesture, then re-check the geometry.
    handle = home.locator('.nodehead')
    before = handle.bounding_box()
    page.mouse.move(before['x'] + 40, before['y'] + 12)
    page.mouse.down()
    page.mouse.move(before['x'] + 100, before['y'] + 60, steps=8)
    page.mouse.up()
    moved = inspect()
    print(f"Arrow geometry after dragging: {moved}", flush=True)
    assert moved['withinButton'] and moved['overlayStacking'], f"Arrow failed after dragging Home: {moved}"
    assert abs(moved['start']['x'] - result['start']['x']) > 15, f"Arrow did not move with Home: {moved}"
    assert not errors, f"JavaScript errors after interactions: {errors}"

    Path("test-artifacts").mkdir(exist_ok=True)
    page.screenshot(path="test-artifacts/canvas.png", full_page=True)
    browser.close()
print("Canvas smoke test passed")

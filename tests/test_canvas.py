from pathlib import Path
import sys
import traceback
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    # Preserve browser evidence even if any assertion fails before the final screenshot.
    previous_hook = sys.excepthook
    def save_failure(exc_type, exc_value, exc_tb):
        Path("test-artifacts").mkdir(exist_ok=True)
        try:
            page.screenshot(path="test-artifacts/canvas-failure.png", full_page=True, timeout=5000)
            Path("test-artifacts/page.html").write_text(page.content(), encoding="utf-8")
        except Exception as capture_error:
            print(f"Could not capture failure evidence: {capture_error}", file=sys.stderr)
        previous_hook(exc_type, exc_value, exc_tb)
    sys.excepthook = save_failure
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
    # Multiple outgoing links must be individually selectable, not stacked on one anchor.
    anchors = page.locator('#connectionPaths path[marker-end*="nav-arrow"]').evaluate_all(
        "(paths) => paths.map(p => { const a=p.getPointAtLength(0); return [a.x,a.y] })"
    )
    assert len(anchors) == 2 and anchors[0] != anchors[1], f"Outgoing links overlap at origin: {anchors}"
    assert page.locator('#connectionPaths .link-hit[data-link]').count() == 2
    assert 'LIGHTS_ON' in page.locator('#actionList').inner_text(), "TCP action missing"
    page.locator('[data-action-up="2"]').click()
    assert page.locator('.multi-action').count() == 3, "Reorder dropped an action"
    # After moving TCP up, remove TCP (index 1), preserving Navigate + Popup.
    page.locator('[data-action-remove="1"]').click()
    assert page.locator('.multi-action').count() == 2, "Remove should delete one action only"
    assert 'Navigate to Page' in page.locator('.multi-action').first.inner_text()
    assert 'Info Popup' in page.locator('.multi-action').last.inner_text()

    # Edit one existing action and preserve the other action and its ordering.
    page.locator('[data-action-edit="0"]').click()
    assert page.locator('#applyBehavior').inner_text() == 'Save Action'
    page.locator('#behaviorTarget').click()
    page.locator('#targetOptions [data-target-id]', has_text='Details').click()
    page.locator('#applyBehavior').click()
    assert page.locator('.multi-action').count() == 2, "Editing duplicated or removed actions"
    assert 'Details' in page.locator('.multi-action').first.inner_text(), "Edited target was not saved"
    assert 'Info Popup' in page.locator('.multi-action').last.inner_text(), "Other action was changed"
    assert page.locator('#connectionPaths path[marker-end*="nav-arrow"]').count() == 2, "Action editing lost links"

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
    # Clicking a Canvas connection must show its own Inspector, even if the button was selected.
    home.locator('.mockbutton').click()
    page.locator('#connectionPaths .link-hit[data-link]').first.dispatch_event('pointerdown', {'button': 0})
    assert page.locator('#editLink').count() == 1, "Canvas connection did not open link Inspector"
    page.locator('#editLink').click()
    assert page.locator('#applyBehavior').inner_text() == 'Save Action', "Canvas Edit Action did not open the selected action"
    page.locator('#cancelActionEdit').click()
    assert page.locator('#applyBehavior').inner_text() == '+ Add Action', "Cancel edit did not reset form"

    # Select the second of two outgoing connections and verify it maps to Popup,
    # then delete only that connection without changing Navigate.
    page.locator('#connectionPaths .link-hit[data-link]').nth(1).dispatch_event('pointerdown', {'button': 0})
    assert 'Info Popup' in page.locator('#details').inner_text(), "Second connection selected wrong action"
    page.locator('#deleteLink').click()
    assert page.locator('#connectionPaths .link-hit[data-link]').count() == 1, "Deleting one connection removed the wrong number"
    home.locator('.mockbutton').click()
    assert page.locator('.multi-action').count() == 1
    assert 'Details' in page.locator('.multi-action').first.inner_text(), "Navigate action was lost"

    # Undo must restore the removed popup action and clear stale link selection.
    page.keyboard.press('Control+z')
    assert page.locator('#connectionPaths .link-hit[data-link]').count() == 2, "Undo did not restore deleted link"
    assert page.locator('#editLink').count() == 0, "Undo retained stale link Inspector"
    home.locator('.mockbutton').click()
    assert page.locator('.multi-action').count() == 2, "Undo did not restore ordered button actions"

    # Explicit Save must survive a reload with action types, order and targets intact.
    page.locator('#save').click()
    page.reload()
    page.wait_for_selector('.node.page')
    home = page.locator('.node.page').filter(has=page.locator('.nodehead', has_text='Home'))
    home.locator('.mockbutton').click()
    assert page.locator('.multi-action').count() == 2, "Saved actions missing after reload"
    assert 'Details' in page.locator('.multi-action').first.inner_text()
    assert 'Info Popup' in page.locator('.multi-action').last.inner_text()
    assert page.locator('#connectionPaths .link-hit[data-link]').count() == 2
    assert not errors, f"JavaScript errors after interactions: {errors}"

    Path("test-artifacts").mkdir(exist_ok=True)
    page.screenshot(path="test-artifacts/canvas.png", full_page=True)
    browser.close()
print("Canvas smoke test passed")

import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Emulate Pixel 5
        device = p.devices['Pixel 5']
        context = await browser.new_context(**device)
        page = await context.new_page()

        # Get the absolute path to index.html
        cwd = os.getcwd()
        url = f"file://{cwd}/index.html"

        print(f"Loading {url} in mobile emulation...")
        await page.goto(url)

        # Wait for blockly to load
        await page.wait_for_selector("#blocklyDiv")

        # 1. Verify Tab Bar exists
        tab_bar = page.locator("#mobileTabBar")
        if await tab_bar.is_visible():
            print("Mobile Tab Bar is visible.")
        else:
            print("Error: Mobile Tab Bar is NOT visible.")

        # 2. Verify Editor is default active
        pane_left = page.locator("#paneLeft")
        pane_right = page.locator("#paneRight")

        if await pane_left.is_visible() and not await pane_right.is_visible():
            print("Default view is Editor (Left Pane).")
        else:
             print(f"Left Pane Visible: {await pane_left.is_visible()}")
             print(f"Right Pane Visible: {await pane_right.is_visible()}")

        # 3. Click Output Tab
        print("Clicking Output Tab...")
        await page.click("#tabOutput")

        # 4. Verify Output is active
        # Note: Playwright's is_visible checks style visibility.
        if await pane_right.is_visible() and not await pane_left.is_visible():
            print("Switched to Output View successfully.")
        else:
            print("Error switching tabs.")

        await page.screenshot(path="screenshot_mobile_tabs.png")
        print("Screenshot saved.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to index.html
        cwd = os.getcwd()
        url = f"file://{cwd}/index.html"

        print(f"Loading {url}...")
        await page.goto(url)

        # Wait for blockly to load
        await page.wait_for_selector("#blocklyDiv")

        # Screenshot Desktop
        await page.set_viewport_size({"width": 1280, "height": 800})
        await page.screenshot(path="screenshot_desktop_before.png")
        print("Desktop screenshot saved.")

        # Screenshot Mobile
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.screenshot(path="screenshot_mobile_before.png")
        print("Mobile screenshot saved.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def debug_consensus_browser_hold():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        page = await browser.new_page()
        await page.goto("https://www.scoresandodds.com/mlb/consensus-picks", timeout=60000)

        print("✅ Page open. Take your time.")
        print("🔎 Right-click on Bet % or team row → Inspect → Copy class name or outerHTML.")
        print("⏳ Browser will stay open until you CTRL+C this script.")

        while True:
            await asyncio.sleep(60)  # keep the browser alive

asyncio.run(debug_consensus_browser_hold())

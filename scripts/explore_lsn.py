#!/usr/bin/env python3
"""
Explore LSN-Online database with Playwright to reverse-engineer the API.
Captures all network requests and responses.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data" / "lsn_exploration"

async def main():
    from playwright.async_api import async_playwright

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    requests_log = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="de-DE"
        )
        page = await context.new_page()

        # Capture all network requests
        async def log_request(request):
            requests_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "request",
                "method": request.method,
                "url": request.url,
                "headers": dict(request.headers),
                "post_data": request.post_data,
            })
            print(f">>> {request.method} {request.url[:80]}")

        async def log_response(response):
            content_type = response.headers.get("content-type", "")
            body = None
            if "text" in content_type or "json" in content_type or "html" in content_type:
                try:
                    body = await response.text()
                    if len(body) > 5000:
                        body = body[:5000] + "... [truncated]"
                except:
                    pass

            requests_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "response",
                "url": response.url,
                "status": response.status,
                "headers": dict(response.headers),
                "body_preview": body[:500] if body else None,
            })
            print(f"<<< {response.status} {response.url[:80]}")

        page.on("request", log_request)
        page.on("response", log_response)

        print("=" * 60)
        print("STEP 1: Load main page")
        print("=" * 60)
        await page.goto("https://www1.nls.niedersachsen.de/statistik/default.asp")
        await page.screenshot(path=DATA_DIR / "01_start.png")

        print("\n" + "=" * 60)
        print("STEP 2: Click WEITER to start session")
        print("=" * 60)
        await page.click('input[value="WEITER"]')
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=DATA_DIR / "02_after_weiter.png")

        # Get the main frame structure
        frames = page.frames
        print(f"\nFrames found: {len(frames)}")
        for i, frame in enumerate(frames):
            print(f"  Frame {i}: {frame.name} - {frame.url[:60] if frame.url else 'no url'}")

        print("\n" + "=" * 60)
        print("STEP 3: Explore frame structure")
        print("=" * 60)

        # Get page HTML to understand structure
        html = await page.content()
        with open(DATA_DIR / "02_page_structure.html", "w") as f:
            f.write(html)

        # Try to find the navigation frame
        try:
            # The site uses framesets - let's navigate the frames
            main_frame = page.frame("haupt")
            if main_frame:
                print("Found 'haupt' frame")
                await main_frame.wait_for_load_state("networkidle")
                main_html = await main_frame.content()
                with open(DATA_DIR / "03_haupt_frame.html", "w") as f:
                    f.write(main_html)
                await page.screenshot(path=DATA_DIR / "03_haupt_frame.png")
        except Exception as e:
            print(f"Error with haupt frame: {e}")

        print("\n" + "=" * 60)
        print("STEP 4: Navigate to Finanzen section")
        print("=" * 60)

        # Try direct URL access to table selection
        await page.goto("https://www1.nls.niedersachsen.de/statistik/html/default.asp")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=DATA_DIR / "04_default_html.png")

        # Try the table generation directly
        print("\n" + "=" * 60)
        print("STEP 5: Try direct table access")
        print("=" * 60)

        # Go to the table parameter page
        await page.goto("https://www1.nls.niedersachsen.de/statistik/html/tabauswahl.asp?G=9")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=DATA_DIR / "05_tabauswahl.png")
        tab_html = await page.content()
        with open(DATA_DIR / "05_tabauswahl.html", "w") as f:
            f.write(tab_html)

        # Try clicking on a specific table
        print("\n" + "=" * 60)
        print("STEP 6: Access Steuereinnahmen table Z9200001")
        print("=" * 60)

        # Navigate to table parameter page
        await page.goto("https://www1.nls.niedersachsen.de/statistik/html/mustertabelle.asp?DT=Z9200001")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=DATA_DIR / "06_mustertabelle.png")
        muster_html = await page.content()
        with open(DATA_DIR / "06_mustertabelle.html", "w") as f:
            f.write(muster_html)

        print("\n" + "=" * 60)
        print("STEP 7: Fill in parameters for Nordstemmen")
        print("=" * 60)

        # Check for form elements
        forms = await page.query_selector_all("form")
        print(f"Forms found: {len(forms)}")

        inputs = await page.query_selector_all("input")
        print(f"Inputs found: {len(inputs)}")
        for inp in inputs[:20]:
            name = await inp.get_attribute("name")
            type_ = await inp.get_attribute("type")
            value = await inp.get_attribute("value")
            print(f"  Input: name={name}, type={type_}, value={value}")

        selects = await page.query_selector_all("select")
        print(f"Selects found: {len(selects)}")
        for sel in selects[:10]:
            name = await sel.get_attribute("name")
            print(f"  Select: name={name}")

        # Save all requests
        with open(DATA_DIR / "network_log.json", "w") as f:
            json.dump(requests_log, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(requests_log)} network requests to network_log.json")
        print(f"Screenshots saved to {DATA_DIR}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

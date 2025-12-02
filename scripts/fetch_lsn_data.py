#!/usr/bin/env python3
"""
Script zum Abrufen von Gemeindefinanzdaten von der LSN-Online Datenbank
mittels Playwright Browser-Automatisierung.

Verwendung:
    pip install playwright pandas openpyxl
    playwright install chromium
    python fetch_lsn_data.py

Ausgabe:
    - data/lsn_gemeindefinanzen_nordstemmen.csv
    - data/lsn_gemeindefinanzen_nordstemmen.xlsx
"""

import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import re

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Playwright nicht installiert. Bitte ausführen:")
    print("  pip install playwright")
    print("  playwright install chromium")
    exit(1)

# Konfiguration
LSN_URL = "https://www1.nls.niedersachsen.de/statistik/"
GEMEINDE_NAME = "Nordstemmen"
GEMEINDE_SCHLUESSEL = "03254035"  # AGS (Amtlicher Gemeindeschlüssel)
DATA_DIR = Path(__file__).parent.parent / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"


class LSNScraper:
    """Scraper für die LSN-Online Datenbank."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.data = []

    async def start(self):
        """Startet den Browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="de-DE"
        )
        self.page = await self.context.new_page()
        print("Browser gestartet")

    async def stop(self):
        """Beendet den Browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser beendet")

    async def init_session(self):
        """Initialisiert die Session auf der Hauptseite."""
        print(f"Lade Hauptseite: {LSN_URL}")
        await self.page.goto(LSN_URL, wait_until="networkidle")
        await asyncio.sleep(3)  # Warte auf JavaScript

        # Mache Screenshot für Debugging
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        await self.page.screenshot(path=SCREENSHOTS_DIR / "01_hauptseite.png")
        print("Session initialisiert")

    async def navigate_to_gemeindefinanzen(self):
        """
        Navigiert zum Bereich Gemeindefinanzen.
        Die Navigation erfolgt über das linke Menü.
        """
        print("Navigiere zu Gemeindefinanzen...")

        # Die LSN verwendet Frames - wir müssen in den richtigen Frame wechseln
        try:
            # Warte auf Frames
            await asyncio.sleep(2)

            # Suche nach dem Navigations-Frame (links.asp)
            frames = self.page.frames
            print(f"Gefundene Frames: {len(frames)}")

            for frame in frames:
                frame_url = frame.url
                print(f"  Frame URL: {frame_url}")

                if "links.asp" in frame_url or "navigation" in frame_url.lower():
                    # Klicke auf "Finanzen" oder "Gemeindefinanzen"
                    try:
                        await frame.click("text=Finanzen", timeout=5000)
                        print("Klick auf 'Finanzen' erfolgreich")
                        await asyncio.sleep(2)
                    except:
                        print("'Finanzen' nicht gefunden, suche Alternativen...")

            await self.page.screenshot(path=SCREENSHOTS_DIR / "02_nach_navigation.png")

        except Exception as e:
            print(f"Navigationsfehler: {e}")
            await self.page.screenshot(path=SCREENSHOTS_DIR / "error_navigation.png")

    async def search_gemeinde(self, name: str = GEMEINDE_NAME):
        """Sucht nach der Gemeinde."""
        print(f"Suche Gemeinde: {name}")

        try:
            # Suche nach Eingabefeld für Gemeindesuche
            search_input = await self.page.query_selector('input[type="text"]')
            if search_input:
                await search_input.fill(name)
                await self.page.keyboard.press("Enter")
                await asyncio.sleep(2)

            await self.page.screenshot(path=SCREENSHOTS_DIR / "03_gemeindesuche.png")

        except Exception as e:
            print(f"Suchfehler: {e}")

    async def extract_table_data(self) -> list:
        """Extrahiert Tabellendaten von der aktuellen Seite."""
        print("Extrahiere Tabellendaten...")

        tables = []

        try:
            # Suche nach Tabellen
            table_elements = await self.page.query_selector_all("table")
            print(f"Gefundene Tabellen: {len(table_elements)}")

            for i, table in enumerate(table_elements):
                rows = await table.query_selector_all("tr")
                table_data = []

                for row in rows:
                    cells = await row.query_selector_all("td, th")
                    row_data = []
                    for cell in cells:
                        text = await cell.inner_text()
                        row_data.append(text.strip())
                    if row_data:
                        table_data.append(row_data)

                if table_data:
                    tables.append(table_data)
                    print(f"  Tabelle {i+1}: {len(table_data)} Zeilen")

        except Exception as e:
            print(f"Extraktionsfehler: {e}")

        return tables

    async def download_excel_if_available(self):
        """Versucht Excel-Export zu nutzen, falls verfügbar."""
        print("Suche Excel-Export-Option...")

        try:
            # Suche nach Excel/Download Button
            excel_button = await self.page.query_selector('a:has-text("Excel"), button:has-text("Excel"), a:has-text("Download")')

            if excel_button:
                print("Excel-Export gefunden, starte Download...")

                # Warte auf Download
                async with self.page.expect_download() as download_info:
                    await excel_button.click()

                download = await download_info.value
                download_path = DATA_DIR / f"lsn_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                await download.save_as(download_path)
                print(f"Download gespeichert: {download_path}")
                return download_path

        except Exception as e:
            print(f"Kein Excel-Export verfügbar: {e}")

        return None

    async def scrape_gemeindefinanzen(self) -> dict:
        """
        Hauptfunktion: Scrapt Gemeindefinanzdaten.
        Gibt strukturierte Daten zurück.
        """
        result = {
            "metadata": {
                "gemeinde": GEMEINDE_NAME,
                "ags": GEMEINDE_SCHLUESSEL,
                "scraped_at": datetime.now().isoformat(),
                "source": "LSN-Online Datenbank"
            },
            "tables": [],
            "raw_text": "",
            "status": "unknown"
        }

        try:
            await self.start()
            await self.init_session()
            await self.navigate_to_gemeindefinanzen()
            await self.search_gemeinde()

            # Extrahiere Daten
            tables = await self.extract_table_data()
            result["tables"] = tables

            # Versuche Excel-Download
            excel_path = await self.download_excel_if_available()
            if excel_path:
                result["excel_file"] = str(excel_path)

            # Hole gesamten Seitentext
            result["raw_text"] = await self.page.inner_text("body")
            result["status"] = "success"

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            print(f"Scraping-Fehler: {e}")

        finally:
            await self.stop()

        return result


def parse_lsn_tables_to_dataframe(tables: list) -> pd.DataFrame:
    """Konvertiert extrahierte Tabellen zu einem DataFrame."""
    all_rows = []

    for table in tables:
        if len(table) < 2:
            continue

        # Erste Zeile als Header
        headers = table[0]

        for row in table[1:]:
            if len(row) == len(headers):
                row_dict = dict(zip(headers, row))
                all_rows.append(row_dict)

    if all_rows:
        return pd.DataFrame(all_rows)
    return pd.DataFrame()


async def main():
    """Hauptprogramm."""
    print("=" * 60)
    print("LSN-Online Datenbank Scraper für Gemeinde Nordstemmen")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    scraper = LSNScraper(headless=True)  # False für Debugging
    result = await scraper.scrape_gemeindefinanzen()

    # Speichere Rohdaten
    json_path = DATA_DIR / "lsn_raw_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        # Tables können nicht direkt serialisiert werden wenn leer
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nRohdaten gespeichert: {json_path}")

    # Konvertiere zu DataFrame
    if result["tables"]:
        df = parse_lsn_tables_to_dataframe(result["tables"])
        if not df.empty:
            csv_path = DATA_DIR / "lsn_gemeindefinanzen_nordstemmen.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8")
            print(f"CSV gespeichert: {csv_path}")

            xlsx_path = DATA_DIR / "lsn_gemeindefinanzen_nordstemmen.xlsx"
            df.to_excel(xlsx_path, index=False)
            print(f"Excel gespeichert: {xlsx_path}")

    print(f"\nStatus: {result['status']}")
    if result.get("error"):
        print(f"Fehler: {result['error']}")

    print("\nScreenshots wurden in data/screenshots/ gespeichert")
    print("\nHinweis: Die LSN-Datenbank erfordert manuelle Navigation.")
    print("Bei Problemen führen Sie das Script mit headless=False aus")
    print("um die Browser-Interaktion zu beobachten.")


if __name__ == "__main__":
    asyncio.run(main())

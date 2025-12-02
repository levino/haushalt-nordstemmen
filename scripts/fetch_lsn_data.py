#!/usr/bin/env python3
"""
Script zum Abrufen von Gemeindefinanzdaten von der LSN-Online Datenbank.

Zwei Methoden verfügbar:
1. API-basiert (requests) - Schneller, für einfache Abfragen
2. Browser-basiert (Playwright) - Für komplexe Navigationen

Verwendung:
    pip install requests beautifulsoup4 pandas openpyxl
    python fetch_lsn_data.py

    # Optional für Browser-Automatisierung:
    pip install playwright
    playwright install chromium
    python fetch_lsn_data.py --browser

Ausgabe:
    - data/lsn_steuereinnahmen_nordstemmen.csv
    - data/lsn_steuereinnahmen_nordstemmen.xlsx
"""

import argparse
import re
import time
from pathlib import Path
from datetime import datetime
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Konfiguration
LSN_BASE_URL = "https://www1.nls.niedersachsen.de/statistik"
GEMEINDE_NAME = "Nordstemmen"
GEMEINDE_LSN_ID = "254026000"  # LSN-interne ID
GEMEINDE_KURZFORM = "254026"
GEMEINDE_AGS = "03254035"  # Amtlicher Gemeindeschlüssel
DATA_DIR = Path(__file__).parent.parent / "data"

# Relevante Tabellen für Kommunalfinanzen
TABLES = {
    "Z9200001": "Steuereinnahmen (Zeitreihe ab 1983)",
    "K9200001": "Steuereinnahmen (Einzeljahr)",
    "Z9200002": "Steuerkraft und Hebesätze (Zeitreihe)",
    "K9200002": "Steuerkraft und Hebesätze (Einzeljahr)",
}


class LSNApiClient:
    """
    Client für die LSN-Online API.

    Nutzt direkte HTTP-Anfragen basierend auf Reverse-Engineering
    der Web-Oberfläche.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self._session_initialized = False

    def start_session(self) -> bool:
        """Initialisiert eine LSN-Session."""
        print("Starte LSN-Session...")
        try:
            # Schritt 1: Hauptseite laden
            response = self.session.get(f"{LSN_BASE_URL}/default.asp")
            if not response.ok:
                print(f"Fehler beim Laden der Hauptseite: {response.status_code}")
                return False

            # Schritt 2: Session aktivieren durch Form-Submit
            response = self.session.post(
                f"{LSN_BASE_URL}/default.asp",
                data={"LOGIN1": "WEITER"},
                allow_redirects=True
            )

            if response.ok:
                self._session_initialized = True
                print("Session erfolgreich initialisiert")
                return True

        except Exception as e:
            print(f"Session-Fehler: {e}")

        return False

    def fetch_table(
        self,
        table_id: str,
        region_id: str = GEMEINDE_LSN_ID,
        level: int = 5  # 5 = Mitgliedsgemeinde
    ) -> tuple[str, str]:
        """
        Ruft eine Tabelle für eine Region ab.

        Args:
            table_id: Tabellen-ID (z.B. Z9200001)
            region_id: LSN-Regions-ID (z.B. 254026000)
            level: Gebietsebene (1-5)

        Returns:
            Tuple aus (HTML-Content, Download-URL)
        """
        if not self._session_initialized:
            self.start_session()

        print(f"Rufe Tabelle {table_id} für Region {region_id} ab...")

        # POST an mustertabelle.asp
        response = self.session.post(
            f"{LSN_BASE_URL}/html/mustertabelle.asp",
            data={
                "DT": table_id,
                "UG": region_id,
                "LN": str(level),
                "LN2": "1",
            }
        )

        if not response.ok:
            print(f"Fehler bei Tabellenabfrage: {response.status_code}")
            return "", ""

        # Extrahiere Redirect-URL aus Meta-Refresh
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find("meta", attrs={"http-equiv": "refresh"})

        if not meta:
            print("Keine Redirect-URL gefunden")
            return response.text, ""

        match = re.search(r"url='([^']+)'", meta.get("content", ""))
        if not match:
            print("Konnte Redirect-URL nicht parsen")
            return response.text, ""

        result_path = match.group(1)
        result_url = f"{LSN_BASE_URL}{result_path}"

        # Warte auf Tabellen-Generierung
        print("Warte auf Tabellen-Generierung...")
        time.sleep(2)

        # Lade Ergebnis
        result_response = self.session.get(result_url)

        if not result_response.ok:
            print(f"Fehler beim Laden des Ergebnisses: {result_response.status_code}")
            return "", ""

        # Extrahiere Download-URL für ZIP
        result_soup = BeautifulSoup(result_response.text, "html.parser")
        download_link = result_soup.find("a", href=re.compile(r"\.zip$"))
        download_url = ""
        if download_link:
            download_url = f"{LSN_BASE_URL}{download_link['href']}"

        return result_response.text, download_url

    def parse_html_table(self, html_content: str) -> pd.DataFrame:
        """Parst eine HTML-Tabelle zu einem DataFrame."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Finde die Haupt-Datentabelle
        tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            if len(rows) < 5:  # Mindestens Header + Daten
                continue

            data = []
            headers = None

            for row in rows:
                cells = row.find_all(["th", "td"])
                cell_texts = [cell.get_text(strip=True) for cell in cells]

                if not any(cell_texts):
                    continue

                # Erster relevanter Header hat "Jahr" oder "Niedersachsen"
                if headers is None and any("Jahr" in t or "Niedersachsen" in t for t in cell_texts):
                    headers = cell_texts
                    continue

                # Datenzeilen enthalten Jahreszahlen
                if headers and any(re.match(r"^\d{4}$", t.strip()) for t in cell_texts):
                    data.append(cell_texts)

            if data and headers:
                # Bereinige Header
                headers = [h.replace("\n", " ").replace("\r", "").strip() for h in headers]

                # Erstelle DataFrame
                df = pd.DataFrame(data, columns=headers[:len(data[0])] if len(headers) >= len(data[0]) else None)
                return df

        return pd.DataFrame()

    def download_zip(self, url: str, output_path: Path) -> bool:
        """Lädt eine ZIP-Datei herunter."""
        try:
            response = self.session.get(url)
            if response.ok:
                output_path.write_bytes(response.content)
                print(f"ZIP gespeichert: {output_path}")
                return True
        except Exception as e:
            print(f"Download-Fehler: {e}")
        return False


def fetch_steuereinnahmen_zeitreihe(client: LSNApiClient) -> pd.DataFrame:
    """
    Ruft die Steuereinnahmen-Zeitreihe für Nordstemmen ab.
    Tabelle Z9200001 enthält Daten ab 1983.
    """
    html, download_url = client.fetch_table("Z9200001")

    if not html:
        return pd.DataFrame()

    # Parse HTML
    df = client.parse_html_table(html)

    if df.empty:
        # Fallback: Versuche ZIP-Download
        if download_url:
            zip_path = DATA_DIR / "lsn_steuereinnahmen.zip"
            if client.download_zip(download_url, zip_path):
                print(f"ZIP heruntergeladen: {zip_path}")
                print("Bitte manuell extrahieren und Excel-Datei öffnen")

    return df


def main_api():
    """Hauptfunktion für API-basierten Abruf."""
    print("=" * 60)
    print("LSN-Online Datenbank - API-Client")
    print(f"Gemeinde: {GEMEINDE_NAME} ({GEMEINDE_AGS})")
    print(f"LSN-ID: {GEMEINDE_LSN_ID}")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    client = LSNApiClient()

    if not client.start_session():
        print("Konnte keine Session starten!")
        return

    # Abruf Steuereinnahmen-Zeitreihe
    print("\n--- Steuereinnahmen (Zeitreihe) ---")
    df = fetch_steuereinnahmen_zeitreihe(client)

    if not df.empty:
        # Speichere als CSV
        csv_path = DATA_DIR / "lsn_steuereinnahmen_nordstemmen.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"CSV gespeichert: {csv_path}")

        # Speichere als Excel
        xlsx_path = DATA_DIR / "lsn_steuereinnahmen_nordstemmen.xlsx"
        df.to_excel(xlsx_path, index=False)
        print(f"Excel gespeichert: {xlsx_path}")

        # Zeige Vorschau
        print(f"\nDaten-Vorschau ({len(df)} Zeilen):")
        print(df.head(10).to_string())
    else:
        print("Keine Daten extrahiert")
        print("Versuche Browser-Modus: python fetch_lsn_data.py --browser")

    # Speichere Metadaten
    metadata = {
        "gemeinde": GEMEINDE_NAME,
        "ags": GEMEINDE_AGS,
        "lsn_id": GEMEINDE_LSN_ID,
        "tabelle": "Z9200001",
        "beschreibung": "Steuereinnahmen (Zeitreihe)",
        "abgerufen_am": datetime.now().isoformat(),
        "quelle": "LSN-Online Datenbank",
        "url": f"{LSN_BASE_URL}/"
    }

    meta_path = DATA_DIR / "lsn_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"\nMetadaten gespeichert: {meta_path}")


async def main_browser():
    """Hauptfunktion für Browser-basierten Abruf mit Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright nicht installiert!")
        print("Installation: pip install playwright && playwright install chromium")
        return

    print("=" * 60)
    print("LSN-Online Datenbank - Browser-Modus (Playwright)")
    print(f"Gemeinde: {GEMEINDE_NAME}")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    screenshots_dir = DATA_DIR / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=True für Server
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="de-DE"
        )
        page = await context.new_page()

        try:
            # 1. Startseite laden
            print("Lade Startseite...")
            await page.goto(f"{LSN_BASE_URL}/default.asp")
            await page.screenshot(path=screenshots_dir / "01_start.png")

            # 2. Session starten
            print("Starte Session...")
            await page.click('input[value="WEITER"]')
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=screenshots_dir / "02_hauptseite.png")

            # 3. Navigiere zu Menü "Staat & Gesellschaft"
            print("Navigiere zu Staat & Gesellschaft...")
            frame = page.frame_locator("frame[name='haupt']").frame_locator("iframe")
            await frame.get_by_role("button", name="Staat & Gesellschaft").click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=screenshots_dir / "03_staat_gesellschaft.png")

            # 4. Finde und klicke auf Steuereinnahmen-Tabelle
            print("Suche Steuereinnahmen-Tabelle...")
            # Die Tabelle wird via JavaScript geladen
            await frame.get_by_text("Z9200001").click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=screenshots_dir / "04_tabelle_param.png")

            # 5. Wähle Nordstemmen
            print(f"Wähle {GEMEINDE_NAME}...")
            # Setze Ebene auf Mitgliedsgemeinde
            await frame.get_by_text("Mitgliedsgemeinde").click()
            await page.wait_for_timeout(2000)

            # Filter auf Nordstemmen
            await frame.locator('input[name="RANGE0"]').fill(GEMEINDE_KURZFORM)
            await frame.locator('input[name="RANGE1"]').fill(GEMEINDE_KURZFORM)
            await frame.get_by_text("OK").click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=screenshots_dir / "05_gemeinde_filter.png")

            # 6. Checkbox aktivieren und Tabelle generieren
            await frame.locator(f'input[value="{GEMEINDE_LSN_ID}"]').check()
            # Klicke auf "Weiter" oder ähnlichen Button
            await page.screenshot(path=screenshots_dir / "06_vor_generierung.png")

            print("\n=== HINWEIS ===")
            print("Browser-Modus offen für manuelle Interaktion.")
            print("Screenshots wurden in data/screenshots/ gespeichert.")
            print("Drücke Enter zum Beenden...")
            input()

        except Exception as e:
            print(f"Fehler: {e}")
            await page.screenshot(path=screenshots_dir / "error.png")

        finally:
            await browser.close()


def main():
    """Haupteinstiegspunkt."""
    parser = argparse.ArgumentParser(
        description="LSN-Online Datenbank Scraper für Gemeinde Nordstemmen"
    )
    parser.add_argument(
        "--browser", "-b",
        action="store_true",
        help="Browser-Modus mit Playwright verwenden"
    )

    args = parser.parse_args()

    if args.browser:
        import asyncio
        asyncio.run(main_browser())
    else:
        main_api()


if __name__ == "__main__":
    main()

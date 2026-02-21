# LSN-Online Datenbank - Dokumentation

## Übersicht

Die LSN-Online ist die größte regionalstatistische Datenbank Deutschlands mit über 1000 Tabellen und ca. 90 Millionen geheimhaltungsgeprüften Statistikdaten bis auf Gemeindeebene.

- **URL**: https://www1.nls.niedersachsen.de/statistik/
- **Betreiber**: Landesamt für Statistik Niedersachsen (LSN)
- **Zugang**: Kostenfrei, keine Anmeldung erforderlich

## Technische Architektur

### URL-Struktur

```
https://www1.nls.niedersachsen.de/statistik/
├── default.asp           # Hauptseite (Frame-Container)
├── html/
│   ├── oben.html        # Kopfzeile
│   ├── links.asp        # Navigation (linke Seite)
│   └── haupt.asp        # Hauptinhalt
```

### Session-Verwaltung

Die Datenbank verwendet:
- Cookie-basierte Sessions
- JavaScript für Navigation und Datenabfrage
- Frameset-basiertes Layout

**Hinweis**: Direkter Zugriff auf Unterseiten ohne gültige Session führt zu 404-Fehlern oder Weiterleitungen.

## Verfügbare Themenbereiche

### Kommunale Finanzen (relevant für Gemeindehaushalte)

| Thema | Beschreibung |
|-------|-------------|
| Kommunale Haushaltssystematik | Struktur kommunaler Haushalte |
| Kommunale Jahresrechnungsstatistik | Ist-Werte der Gemeindehaushalte |
| Jahresabschlussstatistik | Öffentliche Fonds und Einrichtungen |
| Schulden- und Finanzvermögensstatistik | Schuldenstand der Kommunen |
| Vierteljährliche kommunale Kassenstatistik | Aktuelle Kassendaten |
| Kommunaler Finanzausgleich | Zuweisungen und Umlagen |

### Weitere Themen

- Bevölkerung (Demografie, Wanderung, Geburten/Sterbefälle)
- Bildung (Schulen, Ausbildung, Hochschulen)
- Wirtschaft (Arbeitsmarkt, Betriebe, Handel)
- Bauen und Wohnen
- Landwirtschaft und Forsten
- Gesundheit und Soziales
- Umwelt und Energie
- Verkehr

## Tabellennummern-System

Die Tabellen sind nach einem alphanumerischen System organisiert:

```
[Buchstabe][Nummer]G

Beispiele:
- A100001G - Bevölkerungsstatistik
- K7100...  - Kommunale Finanzen
- L1...     - Landwirtschaft
```

## Datenexport

Die Datenbank unterstützt Export in:
- Excel-Format (.xlsx)
- PDF-Format
- Bildschirmausgabe (HTML)

## API-Zugang

**Es gibt keine öffentliche REST-API.**

Für programmatischen Zugriff:
1. Browser-Automatisierung (Selenium/Playwright)
2. Session-basiertes Scraping mit Cookie-Handling
3. Anfrage beim LSN für individuelle Datenlieferungen

### Kontakt für Datenabfragen

```
Landesamt für Statistik Niedersachsen
Zentraler Auskunftsdienst
Tel: 0511 9898-1132/1134
E-Mail: auskunft@statistik.niedersachsen.de
```

## Python-Client (Konzept)

```python
"""
LSN-Online Client (Konzept)
Hinweis: Erfordert Selenium oder ähnliche Browser-Automatisierung
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class LSNClient:
    BASE_URL = "https://www1.nls.niedersachsen.de/statistik/"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def _init_session(self):
        """Initialisiere Session über Hauptseite"""
        self.driver.get(self.BASE_URL)
        time.sleep(2)  # Warte auf JavaScript

    def get_table(self, table_id: str) -> pd.DataFrame:
        """
        Lade Tabelle nach ID

        Args:
            table_id: Tabellen-ID (z.B. "K71001G")

        Returns:
            DataFrame mit Tabellendaten
        """
        self._init_session()
        # Navigation zur Tabelle...
        # Export nach Excel...
        # Parse Excel...
        pass

    def search_gemeinde(self, name: str) -> list:
        """
        Suche nach Gemeinde

        Args:
            name: Gemeindename (z.B. "Nordstemmen")

        Returns:
            Liste der gefundenen Gemeinden mit IDs
        """
        pass

    def close(self):
        self.driver.quit()

# Beispielnutzung
if __name__ == "__main__":
    client = LSNClient()
    try:
        # Finanzstatistik für Nordstemmen
        df = client.get_table("K71001G")
        print(df)
    finally:
        client.close()
```

## Alternative Datenquellen

### Für Nordstemmen empfohlen:

1. **MCP Server Nordstemmen** (via Claude Code)
   - Semantische Suche über alle Ratsdokumente seit 2007
   - Zugriff via Claude Code MCP-Integration (Model Context Protocol)

2. **OParl-API Ratsinformationssystem**
   - URL: https://nordstemmen.ratsinfomanagement.net/webservice/oparl/v1.1/
   - Offener Standard für parlamentarische Informationen

3. **Gemeinde-Website**
   - URL: https://www.nordstemmen.de/rathaus-service/finanzen-steuern/haushaltsplaene/
   - Direkte PDF-Downloads

## Quellen

- [LSN-Online Datenbank](https://www.statistik.niedersachsen.de/startseite/datenangebote/lsn_online_datenbank/)
- [Statistische Berichte Niedersachsen](https://www.statistik.niedersachsen.de/startseite/veroffentlichungen/statistische_berichte/)
- [OParl Standard](https://oparl.org/)

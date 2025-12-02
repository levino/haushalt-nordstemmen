---
sidebar_position: 3
---

# LSN-Online Datenbank

Die LSN-Online ist die größte regionalstatistische Datenbank Deutschlands, betrieben vom Landesamt für Statistik Niedersachsen.

## Übersicht

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://www1.nls.niedersachsen.de/statistik/ |
| **Datenpunkte** | ~90 Millionen |
| **Tabellen** | Über 1.000 |
| **Granularität** | Bis Gemeindeebene |
| **Zugang** | Kostenfrei |

## Technische Architektur

Die Datenbank verwendet eine ältere Web-Architektur:

```
https://www1.nls.niedersachsen.de/statistik/
├── default.asp           # Hauptseite (Frame-Container)
├── html/
│   ├── oben.html        # Kopfzeile
│   ├── links.asp        # Navigation
│   └── haupt.asp        # Hauptinhalt
```

### Herausforderungen

1. **Keine öffentliche API** - Nur Web-Oberfläche
2. **Session-basiert** - Erfordert Cookie-Handling
3. **JavaScript-abhängig** - Braucht Browser-Rendering
4. **Frame-basiert** - Komplexe Navigation

## Datenextraktion mit Playwright

Da keine API verfügbar ist, verwenden wir Browser-Automatisierung:

```python
from playwright.async_api import async_playwright

async def scrape_lsn():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Hauptseite laden
        await page.goto("https://www1.nls.niedersachsen.de/statistik/")
        await page.wait_for_load_state("networkidle")

        # Navigation zu Gemeindefinanzen
        # ... (Frame-Navigation erforderlich)

        await browser.close()
```

## Verfügbare Themen für Kommunalfinanzen

| Thema | Beschreibung |
|-------|--------------|
| Kommunale Haushaltssystematik | Struktur kommunaler Haushalte |
| Kommunale Jahresrechnungsstatistik | Ist-Werte der Gemeindehaushalte |
| Vierteljährliche Kassenstatistik | Aktuelle Finanzdaten |
| Schuldenstatistik | Schuldenstand der Kommunen |
| Kommunaler Finanzausgleich | Zuweisungen und Umlagen |

## Gemeindeschlüssel Nordstemmen

```
AGS: 03254035

03  = Niedersachsen
254 = Landkreis Hildesheim
035 = Gemeinde Nordstemmen
```

## Tabellennummern-System

Die LSN verwendet alphanumerische Tabellen-IDs:

```
[Buchstabe][Nummer]G

Beispiele:
- K7100xG - Kommunale Finanzen
- A1xxxG  - Bevölkerung
- L1xxxG  - Landwirtschaft
```

## Script zur Datenextraktion

Vollständiges Script: [`scripts/fetch_lsn_data.py`](https://github.com/levino/haushalt-nordstemmen/blob/main/scripts/fetch_lsn_data.py)

```bash
# Installation
pip install playwright pandas openpyxl
playwright install chromium

# Ausführung
python scripts/fetch_lsn_data.py
```

### Ausgabe

```
data/
├── lsn_raw_data.json           # Extrahierte Rohdaten
├── lsn_gemeindefinanzen.csv    # Tabellarische Daten
├── lsn_gemeindefinanzen.xlsx   # Excel-Export
└── screenshots/                 # Debug-Screenshots
    ├── 01_hauptseite.png
    ├── 02_nach_navigation.png
    └── 03_gemeindesuche.png
```

## Alternative: Manuelle Datenabfrage

Falls die automatisierte Extraktion fehlschlägt:

1. Öffnen Sie https://www1.nls.niedersachsen.de/statistik/
2. Navigieren Sie zu "Finanzen" → "Gemeindefinanzen"
3. Suchen Sie nach "Nordstemmen" (AGS: 03254035)
4. Exportieren Sie die Daten als Excel

## Kontakt LSN

Für individuelle Datenabfragen:

```
Landesamt für Statistik Niedersachsen
Zentraler Auskunftsdienst
Tel: 0511 9898-1132/1134
E-Mail: auskunft@statistik.niedersachsen.de
```

## Bekannte Einschränkungen

1. **Rate Limiting** - Zu viele Anfragen können blockiert werden
2. **Session-Timeout** - Sessions laufen nach Inaktivität ab
3. **Datenformat** - Oft nur visuelle Tabellen, kein strukturiertes Format
4. **Geheimhaltung** - Manche Daten sind aus Datenschutzgründen gesperrt

## Weiterführende Links

- [LSN-Online Portal](https://www.statistik.niedersachsen.de/startseite/datenangebote/lsn_online_datenbank/)
- [Statistische Berichte](https://www.statistik.niedersachsen.de/startseite/veroffentlichungen/statistische_berichte/)
- [Playwright Dokumentation](https://playwright.dev/python/)

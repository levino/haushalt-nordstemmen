---
sidebar_position: 1
---

# Datenquellen - Übersicht

Diese Webseite verwendet ausschließlich öffentliche Datenquellen. Alle Daten können reproduziert werden.

## Primäre Datenquellen

### 1. Ratsinformationssystem Nordstemmen

Das offizielle Ratsinformationssystem der Gemeinde Nordstemmen enthält alle Beschlussvorlagen, Protokolle und Haushaltspläne seit 2007.

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://nordstemmen.ratsinfomanagement.net/ |
| **API** | OParl v1.1 (offener Standard) |
| **Dokumente** | ~18 Jahre, tausende PDFs |
| **Themen** | Haushalt, Bebauung, Beschlüsse |

### 2. MCP Server Nordstemmen

Ein KI-optimierter Zugang zum Ratsinformationssystem mit semantischer Suche.

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://nordstemmen-mcp.levinkeller.de/mcp |
| **Protokoll** | JSON-RPC 2.0 |
| **Features** | Semantische Suche, PDF-Zugriff |

### 3. LSN-Online Datenbank

Die größte regionalstatistische Datenbank Deutschlands vom Landesamt für Statistik Niedersachsen.

| Eigenschaft | Wert |
|-------------|------|
| **URL** | https://www1.nls.niedersachsen.de/statistik/ |
| **Daten** | 90 Mio. Datenpunkte |
| **Granularität** | Bis Gemeindeebene |
| **Themen** | Finanzen, Bevölkerung, Wirtschaft |

## Datenextraktion

### Automatisierte Scripts

```bash
# Repository klonen
git clone https://github.com/levino/haushalt-nordstemmen.git
cd haushalt-nordstemmen

# Python-Abhängigkeiten installieren
pip install -r scripts/requirements.txt

# Daten vom MCP Server abrufen
python scripts/fetch_mcp_data.py

# Daten von LSN extrahieren (erfordert Playwright)
playwright install chromium
python scripts/fetch_lsn_data.py
```

### Ausgabedateien

| Datei | Beschreibung |
|-------|--------------|
| `data/haushalt_nordstemmen.yaml` | Strukturierte Haushaltsdaten |
| `data/haushalt_mcp_raw.json` | Rohdaten vom MCP Server |
| `data/lsn_raw_data.json` | Rohdaten von LSN-Online |

## Datenstruktur

Die Haushaltsdaten sind in YAML strukturiert:

```yaml
ertraege:
  steuern_und_abgaben:
    name: "Steuern und ähnliche Abgaben"
    werte:
      2023: 13783548
      2024: 13446200
      2025: 14173300
    einheit: EUR

aufwendungen:
  personalaufwendungen:
    name: "Personalaufwendungen"
    werte:
      2023: 4692802
      2024: 5023400
      2025: 5423300
    einheit: EUR
```

## Reproduzierbarkeit

Alle Daten können jederzeit neu abgerufen werden. Die Scripts sind idempotent und überschreiben bestehende Daten.

**Hinweis:** Die LSN-Datenbank erfordert Browser-Automatisierung, da keine öffentliche API verfügbar ist.

## Weiterführende Dokumentation

- [MCP Server](/docs/datenquellen/mcp-server) - Technische Details zur API
- [LSN Datenbank](/docs/datenquellen/lsn-datenbank) - Reverse-Engineering Dokumentation

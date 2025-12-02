---
sidebar_position: 1
slug: /
---

# Haushalt der Gemeinde Nordstemmen

Willkommen zur interaktiven Visualisierung des Gemeindehaushalts von **Nordstemmen** im Landkreis Hildesheim, Niedersachsen.

## Was ist diese Seite?

Diese Webseite macht die Finanzen der Gemeinde Nordstemmen transparent und verständlich. Sie zeigt:

- **Woher kommt das Geld?** (Einnahmen)
- **Wofür wird das Geld ausgegeben?** (Ausgaben)
- **Wie entwickeln sich die Finanzen über die Jahre?** (Zeitreihen)

## Aktuelle Haushaltslage

Die Gemeinde Nordstemmen befindet sich seit 2024 in der **Haushaltssicherung**. Das bedeutet, dass die Ausgaben die Einnahmen übersteigen und Maßnahmen zur Haushaltskonsolidierung ergriffen werden müssen.

### Haushalt 2025 auf einen Blick

| Kennzahl | Wert |
|----------|------|
| **Ordentliche Erträge** | 24,1 Mio. EUR |
| **Ordentliche Aufwendungen** | 29,0 Mio. EUR |
| **Ordentliches Ergebnis** | -4,9 Mio. EUR |
| **Investitionen** | 5,9 Mio. EUR |

## Datenquellen

Alle Daten stammen aus öffentlichen Quellen:

1. **[Ratsinformationssystem Nordstemmen](https://nordstemmen.ratsinfomanagement.net/)** - Haushaltspläne und Drucksachen
2. **[Gemeinde Nordstemmen](https://www.nordstemmen.de/)** - Offizielle Veröffentlichungen
3. **[LSN-Online Datenbank](https://www1.nls.niedersachsen.de/statistik/)** - Historische Statistikdaten

## Navigation

- **[Haushalt 2025](/docs/haushalt-2025/uebersicht)** - Aktueller Haushaltsplan
- **[Haushalt 2024](/docs/haushalt-2024/uebersicht)** - Vorjahresvergleich
- **[Zeitreihen](/docs/zeitreihen/uebersicht)** - Entwicklung über mehrere Jahre
- **[Datenquellen](/docs/datenquellen/uebersicht)** - Technische Dokumentation

## Reproduzierbarkeit

Alle Daten und Scripts zur Datenextraktion sind im [GitHub Repository](https://github.com/levino/haushalt-nordstemmen) verfügbar:

```bash
# Daten vom MCP Server abrufen
python scripts/fetch_mcp_data.py

# Daten von LSN-Online extrahieren (erfordert Playwright)
python scripts/fetch_lsn_data.py
```

Die strukturierten Haushaltsdaten sind in [`data/haushalt_nordstemmen.yaml`](https://github.com/levino/haushalt-nordstemmen/blob/main/data/haushalt_nordstemmen.yaml) gespeichert.

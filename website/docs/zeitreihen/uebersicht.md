---
sidebar_position: 1
---

# Zeitreihen - Entwicklung des Haushalts

Diese Seite zeigt die Entwicklung wichtiger Haushaltskennzahlen über mehrere Jahre.

## Gesamtentwicklung 2023-2028

```mermaid
xychart-beta
    title "Erträge vs. Aufwendungen (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" 0 --> 35
    line [24.8, 24.7, 24.1, 24.2, 24.6, 25.0]
    line [24.1, 25.4, 29.0, 29.4, 29.0, 29.4]
```

**Legende:** Obere Linie = Erträge, Untere Linie = Aufwendungen

## Jahresergebnis (Saldo)

```mermaid
xychart-beta
    title "Ordentliches Ergebnis (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" -6 --> 2
    bar [0.7, -0.7, -4.9, -5.2, -4.4, -4.3]
```

| Jahr | Erträge | Aufwendungen | Ergebnis |
|------|---------|--------------|----------|
| 2023 | 24.849.370 | 24.110.625 | +738.745 |
| 2024 | 24.657.000 | 25.381.600 | -724.600 |
| 2025 | 24.083.800 | 28.956.900 | -4.873.100 |
| 2026 | 24.163.400 | 29.350.700 | -5.187.300 |
| 2027 | 24.600.600 | 29.034.800 | -4.434.200 |
| 2028 | 25.028.300 | 29.369.200 | -4.340.900 |

## Steuereinnahmen

```mermaid
xychart-beta
    title "Steuereinnahmen (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" 0 --> 18
    bar [13.8, 13.4, 14.2, 14.4, 14.8, 15.2]
```

| Jahr | Steuern gesamt | Davon Gewerbesteuer |
|------|----------------|---------------------|
| 2023 | 13.783.548 | ca. 3.500.000 |
| 2024 | 13.446.200 | ca. 3.550.000 |
| 2025 | 14.173.300 | ca. 3.800.000 |
| 2026 | 14.360.900 | ca. 3.800.000 |
| 2027 | 14.808.800 | ca. 3.800.000 |
| 2028 | 15.223.600 | ca. 3.800.000 |

## Personalaufwendungen

```mermaid
xychart-beta
    title "Personalaufwendungen (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" 0 --> 7
    bar [4.7, 5.0, 5.4, 5.6, 5.9, 6.0]
```

| Jahr | Personalaufwand | Veränderung zum Vorjahr |
|------|-----------------|-------------------------|
| 2023 | 4.692.802 | - |
| 2024 | 5.023.400 | +7,0% |
| 2025 | 5.423.300 | +8,0% |
| 2026 | 5.595.600 | +3,2% |
| 2027 | 5.866.100 | +4,8% |
| 2028 | 6.036.500 | +2,9% |

**Treiber der Personalkosten:**
- Tarifsteigerungen im öffentlichen Dienst
- Ausbau der Kindertagesbetreuung
- Zusätzliches Personal für neue Aufgaben

## Transferaufwendungen

Die größte Ausgabenposition - hauptsächlich Kreisumlage:

```mermaid
xychart-beta
    title "Transferaufwendungen (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" 0 --> 18
    bar [12.0, 14.2, 15.0, 15.1, 14.8, 14.9]
```

## Investitionen

```mermaid
xychart-beta
    title "Investitionsauszahlungen (in Mio. EUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Millionen EUR" 0 --> 7
    bar [3.7, 4.5, 6.0, 3.0, 1.6, 1.0]
```

| Jahr | Investitionen | Schwerpunkte |
|------|---------------|--------------|
| 2023 | 3.655.756 | Laufende Maßnahmen |
| 2024 | 4.549.000 | Schulen, Kitas |
| 2025 | 5.956.200 | Baumaßnahmen, Kita-Ausbau |
| 2026 | 2.952.700 | Abschluss laufender Projekte |
| 2027 | 1.583.200 | Reduzierte Neuinvestitionen |
| 2028 | 1.032.500 | Konsolidierungsphase |

## Zinsaufwendungen

```mermaid
xychart-beta
    title "Zinsaufwendungen (in TEUR)"
    x-axis [2023, 2024, 2025, 2026, 2027, 2028]
    y-axis "Tausend EUR" 0 --> 1200
    bar [551, 833, 848, 913, 973, 1033]
```

**Trend:** Die Zinslasten steigen aufgrund:
- Höherer Zinssätze am Kapitalmarkt
- Neue Kreditaufnahmen zur Defizitfinanzierung

## Datenquellen

Die Zeitreihen basieren auf:
- Jahresrechnungen (Ist-Werte)
- Haushaltsplänen (Plan-Werte)
- Mittelfristige Finanzplanung

Alle Daten sind in [`data/haushalt_nordstemmen.yaml`](https://github.com/levino/haushalt-nordstemmen/blob/main/data/haushalt_nordstemmen.yaml) dokumentiert.

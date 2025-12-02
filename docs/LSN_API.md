# LSN-Online API Dokumentation

## Übersicht

Die LSN-Online (Landesamt für Statistik Niedersachsen) Datenbank bietet eine Web-basierte API für den Abruf von Statistikdaten. Diese Dokumentation beschreibt das Reverse-Engineering der API.

## Base URL

```
https://www1.nls.niedersachsen.de/statistik
```

## Authentifizierung

Keine Authentifizierung erforderlich. Die Session wird über Cookies verwaltet.

## Session-Flow

### 1. Session initialisieren

```http
POST /default.asp
Content-Type: application/x-www-form-urlencoded

LOGIN1=WEITER
```

Nach diesem Request erhält man ein Session-Cookie (`AL_SESS-S`).

### 2. Navigation-Tree laden

```http
GET /html/haupt_neu.asp?MENU={menu_id}
```

Menü-IDs:
- `17` - EVAS Systematik (alle Tabellen)
- `7` - Statistische Erhebung
- `11` - Leben & Arbeiten
- `12` - Staat & Gesellschaft
- `13` - Wirtschaft & Preise
- `19` - Regionalmonitoring
- `21` - Umwelt & Mobilität

### 3. Tabellen-Parameter laden

```http
GET /html/param_haupt.asp?DT={table_id}&IFR=1&LN={level}&RANGE0={from}&RANGE1={to}
```

Parameter:
- `DT` - Tabellen-ID (z.B. `Z9200001`)
- `IFR` - Iframe-Modus (immer `1`)
- `LN` - Gebietsebene:
  - `0` oder `1` - Land Niedersachsen
  - `2` - Statistische Region
  - `3` - Kreisfreie Stadt / Landkreis
  - `4` - Einheits-/Samtgemeinde
  - `5` - Mitgliedsgemeinde
- `RANGE0`, `RANGE1` - Gebiets-Filter (6-stelliger Schlüssel)

### 4. Tabelle abrufen

```http
POST /html/mustertabelle.asp
Content-Type: application/x-www-form-urlencoded

DT={table_id}&ZUFALL={random}&UG={region_id}&LN={level}&LN2=9&RANGE0={from}&RANGE1={to}&TEXTSORT=
```

Parameter:
- `DT` - Tabellen-ID
- `ZUFALL` - Zufallszahl für Session-Tracking (z.B. `0.932934`)
- `UG` - Region-ID (9-stellig, z.B. `254026000` für Nordstemmen)
- `LN` - Gebietsebene
- `LN2` - Sekundäre Ebene (typisch `9`)
- `TEXTSORT` - Sortierung (`""` = hierarchisch, `"Y"` = alphabetisch)
- `VAW` - Alle auswählen (`"1"` wenn aktiviert)

Response: HTML mit Meta-Refresh zu generierter Ergebnisseite.

### 5. Ergebnis abrufen

```http
GET /Statistik/pool/{table_id}/{generated_filename}.asp
```

Die URL wird aus dem Meta-Refresh der vorherigen Antwort extrahiert.

### 6. Download

```http
GET /Statistik/pool/{table_id}/{generated_filename}.zip
```

Liefert eine ZIP-Datei mit Excel-XML.

## Wichtige Tabellen

### Kommunalfinanzen (EVAS 71321 - Realsteuerstatistik)

| Tabellen-ID | Beschreibung | Zeitraum |
|-------------|--------------|----------|
| `Z9200001` | Steuereinnahmen (Zeitreihe) | 1983 ff. |
| `K9200001` | Steuereinnahmen (Einzeljahr) | aktuell |
| `Z9200002` | Steuerkraft und Hebesätze (Zeitreihe) | 1983 ff. |
| `K9200002` | Steuerkraft und Hebesätze (Einzeljahr) | aktuell |

### Tabelle Z9200001 - Steuereinnahmen

Enthaltene Merkmale (pro Einwohner):
- Einwohner (am 30.06.)
- Steuereinnahmen (netto) insgesamt
- Grundsteuer A
- Grundsteuer B
- Gewerbesteuer (netto)
- Gemeindeanteil an der Einkommensteuer
- Gemeindeanteil an der Umsatzsteuer

## Region-IDs (Beispiele)

| Region | ID | Schlüssel |
|--------|-----|-----------|
| Niedersachsen | `000000000` | `0` |
| Nordstemmen | `254026000` | `254026` |
| Hildesheim (Landkreis) | `254000000` | `254` |

## Beispiel: Nordstemmen Steuereinnahmen abrufen

```bash
# 1. Session starten
curl -c cookies.txt -d "LOGIN1=WEITER" \
  "https://www1.nls.niedersachsen.de/statistik/default.asp"

# 2. Tabelle anfordern
curl -b cookies.txt -d "DT=Z9200001&ZUFALL=0.123&UG=254026000&LN=5&LN2=9" \
  "https://www1.nls.niedersachsen.de/statistik/html/mustertabelle.asp"

# 3. Redirect-URL aus Response extrahieren und abrufen
# 4. ZIP herunterladen
```

## Response-Formate

### HTML-Tabelle

Die generierte HTML-Seite enthält eine formatierte Tabelle mit:
- Copyright-Hinweis
- Tabellenüberschrift
- Spaltennamen (Merkmal-Beschreibungen)
- Datenzeilen

### Excel-XML

Die ZIP-Datei enthält eine Excel-XML-Datei (`.xml` mit `mso-application progid="Excel.Sheet"`), die direkt in Excel geöffnet werden kann.

## Fehlerbehandlung

- **404**: Session abgelaufen oder ungültige Parameter
- **Meta-Refresh zu `/error_path/`**: Bot-Detection oder ungültige Anfrage

## Rate Limiting

Keine bekannten Limits. Empfehlung: 1-2 Sekunden Pause zwischen Anfragen.

## Hinweise

1. Der User-Agent sollte browser-ähnlich sein
2. Cookies müssen zwischen Requests persistiert werden
3. Die generierten URLs sind temporär (ca. 15 Minuten gültig)
4. Die Daten sind öffentlich und dürfen mit Quellenangabe verwendet werden

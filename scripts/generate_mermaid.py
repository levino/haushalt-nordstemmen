#!/usr/bin/env python3
"""
Script zum Generieren von Mermaid Sankey-Diagrammen aus den YAML-Haushaltsdaten.

Verwendung:
    python generate_mermaid.py

Ausgabe:
    - docs/generated/sankey_einnahmen.md
    - docs/generated/sankey_ausgaben.md
"""

import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "website" / "docs" / "generated"


def load_haushalt_data() -> dict:
    """Lädt die Haushaltsdaten aus der YAML-Datei."""
    yaml_path = DATA_DIR / "haushalt_nordstemmen.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_number(value: int) -> str:
    """Formatiert Zahl für Mermaid (in Tausend EUR)."""
    return str(round(value / 1000))


def generate_einnahmen_sankey(data: dict, year: int = 2025) -> str:
    """Generiert Mermaid Sankey für Einnahmen."""
    ertraege = data.get("ertraege", {})

    lines = [
        "```mermaid",
        "sankey-beta",
        "",
        f"%% Einnahmen {year}",
    ]

    for key, item in ertraege.items():
        name = item.get("name", key)
        value = item.get("werte", {}).get(year, 0)
        if value > 0:
            lines.append(f"{name},Haushalt Nordstemmen,{format_number(value)}")

    lines.append("```")
    return "\n".join(lines)


def generate_ausgaben_sankey(data: dict, year: int = 2025) -> str:
    """Generiert Mermaid Sankey für Ausgaben."""
    aufwendungen = data.get("aufwendungen", {})

    lines = [
        "```mermaid",
        "sankey-beta",
        "",
        f"%% Ausgaben {year}",
    ]

    for key, item in aufwendungen.items():
        name = item.get("name", key)
        value = item.get("werte", {}).get(year, 0)
        if value > 0:
            lines.append(f"Haushalt Nordstemmen,{name},{format_number(value)}")

    lines.append("```")
    return "\n".join(lines)


def generate_combined_sankey(data: dict, year: int = 2025) -> str:
    """Generiert kombiniertes Sankey für Ein- und Ausgaben."""
    ertraege = data.get("ertraege", {})
    aufwendungen = data.get("aufwendungen", {})

    lines = [
        "```mermaid",
        "sankey-beta",
        "",
        f"%% Haushalt {year} - Gesamtübersicht",
        "",
        "%% Einnahmen zur Gemeinde",
    ]

    for key, item in ertraege.items():
        name = item.get("name", key)
        value = item.get("werte", {}).get(year, 0)
        if value > 0:
            lines.append(f"{name},Gemeinde Nordstemmen,{format_number(value)}")

    lines.append("")
    lines.append("%% Ausgaben von der Gemeinde")

    for key, item in aufwendungen.items():
        name = item.get("name", key)
        value = item.get("werte", {}).get(year, 0)
        if value > 0:
            lines.append(f"Gemeinde Nordstemmen,{name},{format_number(value)}")

    lines.append("```")
    return "\n".join(lines)


def main():
    """Hauptprogramm."""
    print("Lade Haushaltsdaten...")
    data = load_haushalt_data()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generiere Diagramme für verschiedene Jahre
    for year in [2024, 2025, 2026]:
        print(f"\nGeneriere Diagramme für {year}...")

        # Einnahmen
        einnahmen = generate_einnahmen_sankey(data, year)
        print(f"  Einnahmen Sankey ({year}):")
        print(einnahmen[:200] + "...")

        # Ausgaben
        ausgaben = generate_ausgaben_sankey(data, year)
        print(f"  Ausgaben Sankey ({year}):")
        print(ausgaben[:200] + "...")

        # Kombiniert
        combined = generate_combined_sankey(data, year)

        # Speichere in Datei
        md_content = f"""---
title: Automatisch generierte Sankey-Diagramme {year}
---

# Sankey-Diagramme {year}

Diese Diagramme wurden automatisch aus `data/haushalt_nordstemmen.yaml` generiert.

## Einnahmen

{einnahmen}

## Ausgaben

{ausgaben}

## Gesamtübersicht

{combined}
"""
        output_path = OUTPUT_DIR / f"sankey_{year}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  Gespeichert: {output_path}")

    print("\nFertig!")


if __name__ == "__main__":
    main()

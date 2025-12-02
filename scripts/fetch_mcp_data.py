#!/usr/bin/env python3
"""
Script zum Abrufen von Haushaltsdaten vom MCP Server Nordstemmen.

Verwendung:
    python fetch_mcp_data.py

Ausgabe:
    - data/haushalt_mcp_raw.json  (Rohdaten)
    - data/haushalt_extracted.yaml (Strukturierte Daten)
"""

import json
import requests
import yaml
from pathlib import Path
from datetime import datetime
import re

MCP_URL = "https://nordstemmen-mcp.levinkeller.de/mcp"
DATA_DIR = Path(__file__).parent.parent / "data"


def call_mcp(method: str, params: dict = None) -> dict:
    """Ruft MCP Server JSON-RPC Endpunkt auf."""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    if params:
        payload["params"] = params

    response = requests.post(
        MCP_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def search_haushalt_documents(query: str, limit: int = 10, date_from: str = None) -> list:
    """Sucht nach Haushaltsdokumenten."""
    args = {"query": query, "limit": limit}
    if date_from:
        args["date_from"] = date_from

    result = call_mcp("tools/call", {
        "name": "search_documents",
        "arguments": args
    })

    if "result" in result and "structuredContent" in result["result"]:
        return result["result"]["structuredContent"]["results"]
    return []


def get_paper(reference: str) -> dict:
    """Holt eine Drucksache nach Referenznummer."""
    result = call_mcp("tools/call", {
        "name": "get_paper_by_reference",
        "arguments": {"reference": reference}
    })

    if "result" in result and "structuredContent" in result["result"]:
        return result["result"]["structuredContent"]
    return {}


def extract_numbers_from_text(text: str) -> dict:
    """
    Extrahiert Zahlen aus Haushaltstext.
    Erkennt Muster wie "13.783.548,35" oder "13446200"
    """
    # Pattern für deutsche Zahlendarstellung
    pattern = r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(?:€|EUR)?'
    matches = re.findall(pattern, text)

    numbers = []
    for match in matches:
        # Konvertiere zu Float
        num_str = match.replace('.', '').replace(',', '.')
        try:
            numbers.append(float(num_str))
        except ValueError:
            continue

    return numbers


def fetch_all_haushalt_data():
    """Hauptfunktion: Holt alle Haushaltsdaten."""
    print("Starte Datenabfrage vom MCP Server...")

    all_data = {
        "metadata": {
            "fetched_at": datetime.now().isoformat(),
            "source": MCP_URL,
            "description": "Haushaltsdaten der Gemeinde Nordstemmen"
        },
        "searches": [],
        "papers": []
    }

    # Suchanfragen für verschiedene Haushaltsjahre
    searches = [
        {"query": "Haushaltsplan 2025 Ergebnishaushalt Finanzhaushalt", "date_from": "2024-01-01"},
        {"query": "Haushaltsplan 2024 Ergebnishaushalt", "date_from": "2023-01-01"},
        {"query": "Haushaltsplan 2023 Haushalt", "date_from": "2022-01-01"},
        {"query": "Haushaltsplan 2022 2021 2020", "date_from": "2019-01-01"},
        {"query": "Jahresrechnung Jahresabschluss", "date_from": "2020-01-01"},
        {"query": "Haushaltssicherungskonzept", "date_from": "2023-01-01"},
    ]

    for search in searches:
        print(f"  Suche: {search['query'][:50]}...")
        try:
            results = search_haushalt_documents(
                search["query"],
                limit=10,
                date_from=search.get("date_from")
            )
            all_data["searches"].append({
                "query": search["query"],
                "date_from": search.get("date_from"),
                "result_count": len(results),
                "results": results
            })
        except Exception as e:
            print(f"    Fehler: {e}")

    # Wichtige Drucksachen direkt abrufen
    important_papers = [
        "DS 89/2024",      # Haushaltsplan 2025
        "DS 85/2023",      # Haushaltsplan 2024
        "DS 36/2023",      # Nachtragshaushalt 2023
        "DS 26/2025",      # Jahresabschluss 2024
        "DS 103/2025",     # Haushaltsplan 2026
    ]

    for ref in important_papers:
        print(f"  Hole Drucksache: {ref}...")
        try:
            paper = get_paper(ref)
            if paper:
                all_data["papers"].append(paper)
        except Exception as e:
            print(f"    Fehler: {e}")

    return all_data


def save_data(data: dict):
    """Speichert die Daten."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Rohdaten als JSON
    json_path = DATA_DIR / "haushalt_mcp_raw.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Rohdaten gespeichert: {json_path}")

    # Extrahierte Daten als YAML
    extracted = extract_structured_data(data)
    yaml_path = DATA_DIR / "haushalt_extracted.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(extracted, f, allow_unicode=True, default_flow_style=False)
    print(f"Strukturierte Daten gespeichert: {yaml_path}")


def extract_structured_data(data: dict) -> dict:
    """Extrahiert strukturierte Haushaltsdaten aus den Rohdaten."""
    extracted = {
        "metadata": data["metadata"],
        "dokumente": [],
        "haushaltsjahre": {}
    }

    # Sammle alle gefundenen Dokumente
    seen_hashes = set()
    for search in data.get("searches", []):
        for result in search.get("results", []):
            file_hash = result.get("file_hash", "")
            if file_hash and file_hash not in seen_hashes:
                seen_hashes.add(file_hash)
                extracted["dokumente"].append({
                    "titel": result.get("title", ""),
                    "referenz": result.get("reference", ""),
                    "datum": result.get("date", ""),
                    "pdf_url": result.get("pdf_url", ""),
                    "oparl_id": result.get("oparl_id", ""),
                    "excerpt": result.get("excerpt", "")[:500] if result.get("excerpt") else ""
                })

    return extracted


if __name__ == "__main__":
    data = fetch_all_haushalt_data()
    save_data(data)
    print("\nFertig!")

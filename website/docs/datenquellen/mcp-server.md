---
sidebar_position: 2
---

# MCP Server Nordstemmen

Der MCP (Model Context Protocol) Server bietet einen KI-optimierten Zugang zum Ratsinformationssystem der Gemeinde Nordstemmen.

## Endpunkt

```
https://nordstemmen-mcp.levinkeller.de/mcp
```

**Protokoll:** JSON-RPC 2.0

## Verfügbare Tools

### 1. search_documents

Semantische Suche durch alle Dokumente.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_documents",
    "arguments": {
      "query": "Haushaltsplan 2025",
      "limit": 10,
      "date_from": "2024-01-01"
    }
  },
  "id": 1
}
```

**Parameter:**
- `query` (required): Suchanfrage in natürlicher Sprache
- `limit` (optional): Max. Ergebnisse (1-10, Standard: 5)
- `date_from` (optional): Startdatum (YYYY-MM-DD)
- `date_to` (optional): Enddatum (YYYY-MM-DD)

### 2. get_paper_by_reference

Drucksache nach Referenznummer abrufen.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_paper_by_reference",
    "arguments": {
      "reference": "DS 89/2024"
    }
  },
  "id": 2
}
```

**Formate:**
- `DS 101/2024`
- `101/2024`
- `101-2024`

### 3. search_papers

Strukturierte Suche nach Drucksachen.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_papers",
    "arguments": {
      "title_contains": "Haushaltsplan",
      "limit": 10
    }
  },
  "id": 3
}
```

## Beispiel mit curl

```bash
curl -X POST https://nordstemmen-mcp.levinkeller.de/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_documents",
      "arguments": {
        "query": "Haushaltsplan 2025 Ergebnishaushalt",
        "limit": 5
      }
    },
    "id": 1
  }'
```

## Beispiel mit Python

```python
import requests

MCP_URL = "https://nordstemmen-mcp.levinkeller.de/mcp"

def search_haushalt(query: str, limit: int = 5):
    response = requests.post(MCP_URL, json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "search_documents",
            "arguments": {"query": query, "limit": limit}
        },
        "id": 1
    })
    return response.json()

# Suche nach Haushaltsplan 2025
results = search_haushalt("Haushaltsplan 2025")
for doc in results["result"]["structuredContent"]["results"]:
    print(f"- {doc['title']}: {doc['pdf_url']}")
```

## Rückgabestruktur

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "structuredContent": {
      "results": [
        {
          "title": "Haushaltssatzung und Haushaltsplan 2025",
          "reference": "DS 89/2024",
          "date": "2024-12-17",
          "pdf_url": "https://nordstemmen-mcp.levinkeller.de/pdf/...",
          "oparl_id": "https://nordstemmen.ratsinfomanagement.net/...",
          "score": 0.85,
          "excerpt": "Ergebnishaushalt 2025..."
        }
      ]
    }
  }
}
```

## PDF-Zugriff

PDFs können direkt über die `pdf_url` heruntergeladen werden:

```bash
curl -o haushaltsplan.pdf "https://nordstemmen-mcp.levinkeller.de/pdf/..."
```

## OParl-Standard

Der Server basiert auf dem [OParl-Standard](https://oparl.org/) für parlamentarische Informationssysteme.

**Datenmodell:**
- **Paper** (Drucksache): Beschlussvorlagen, Anträge
- **Meeting** (Sitzung): Rats- und Ausschusssitzungen
- **File** (Datei): PDF-Dokumente

## Datenumfang

- Dokumente seit 2007
- Über 5.000 Drucksachen
- Tausende Sitzungsprotokolle
- Alle Haushaltspläne und Finanzberichte

# RFC-002: Automated Fixture Ingestion (The RIP Protocol)

**STATUS: IMPLEMENTED / ACTIVE**

## 1. Objective
Remove manual data entry from the fixture pipeline by implementing a high-speed HTML parsing system.

## 2. Technical Implementation
The system utilizes `src/fpl_dominator/process_fixtures_html.py` to scrape and structure data from FPL/FFS HTML tables.

### 2.1 The RIP Workflow
1. **Rip:** User copies the OuterHTML of the fixture tables.
2. **Ingest:** `bamf rip fix` (and related commands) captures clipboard content and saves it to the current gameweek vault.
3. **Process:** `process_fixtures_html.py` converts these HTML fragments into structured CSVs.

## 3. Operational Integration
The functionality is exposed via the `bamf` CLI, ensuring that the "Ritual of the Rip" is the primary method for updating the Chimera's world-view.

# BAMF-RFC-001: THE RAPID INGESTION PROTOCOL (RIP) (v1.1)

**Status:** APPROVED (Voyage Initialized) `(⇌)`
**Objective:** Reduce weekly data capture time to < 10 minutes.
**Core Philosophy:** Capture everything, process when ready. **EX DATA, VICTORIA.**

---

## 0. SECURITY & THE VAULT OF SECRETS (MANDATORY)

To command the Chimera from the shadows, we must maintain secure access to the portals of intelligence (FPL & FFS).

- **Credentials Management:** NEVER hardcode logins or passwords in scripts or protocol files.
- **The `.env` Sentinel:** All credentials should reside in a local `.env` file, which is strictly ignored by the git repository.
- **Reference Keys:**
  - `FPL_LOGIN`: Your FPL email/username.
  - `FPL_PASS`: Your FPL password.
  - `FFS_LOGIN`: Your Fantasy Football Scout email/username.
  - `FFS_PASS`: Your FFS password.

---

## I. PRE-FLIGHT: THE VAULT GENESIS
The very first action. No data exists without a home.
1.  **Command:** `bamf init gwN` (where N is the current gameweek).
2.  **Outcome:** Directory structure and placeholder files forged.

---

## II. THE RITUAL OF THE LENS (FFS FIXTURES)
*Estimated Time: 2 Minutes*

1.  **Login to FFS:** Access the [FFS Members area](https://members.fantasyfootballscout.co.uk/season-ticker/).
2.  **Configure:** Select the next gameweek **GW(N+1)**.
3.  **The HTML Rip (via DevTools/Element Picker):**
    *   Find the `<div class="advanced-ticker" ...>` element.
    *   **Overall FDR:** Copy OuterHTML -> Save to `gwN/fixtures_5w.html`.
    *   **Defence FDR:** Copy OuterHTML -> Save to `gwN/fixtures_defence_5w.html`.
    *   **Attack FDR:** Copy OuterHTML -> Save to `gwN/fixtures_attack_5w.html`.
4.  **Execute Transformation:**
    *   **Command:** `bamf process-fixtures gwN`.

---

## III. THE RITUAL OF THE GRID (FPL PLAYERS)
*Estimated Time: 5 Minutes*
**This is the preferred method for high-speed ingestion.**

1.  **Login to FPL:** Access the [FPL Transfers Page](https://fantasy.premierleague.com/transfers).
2.  **Configure:** Ensure **'List View'** is active.
3.  **The HTML Rip (Repeat for GKP, DEF, MID, FWD):**
    *   Select the position filter.
    *   Scroll to the bottom of the list to ensure all players are rendered.
    *   Find the table element (e.g., `<table aria-label="Defenders" ...>`) or its parent div.
    *   **Copy OuterHTML** and save to the corresponding file:
        *   Goalkeepers -> `gwN/goalkeepers.html`
        *   Defenders -> `gwN/defenders.html`
        *   Midfielders -> `gwN/midfielders.html`
        *   Forwards -> `gwN/forwards.html`
4.  **The Squad Price Archive:** 
    *   Select "All Players" or your current squad view.
    *   Copy OuterHTML of the squad table -> Save to `gwN/squad.html`.
5.  **Execute Transformation:**
    *   **Command:** `bamf process-players gwN`.

---

## IV. THE RITUAL OF THE SCROLL (FPL SCREENSHOTS - BACKUP)
*Estimated Time: 2 Minutes*
**Only necessary if the HTML Rip fails.**

1.  **The Price Archive:** Screenshot of the full squad list -> Save to `gwN/squad.png`.
2.  **The Position Archives:** Screenshots of each position list -> Save to `gwN/[pos].png`.

---

## V. THE INTEGRITY CHECK (VERIFICATION)
Before the ritual is considered complete, the Carbon Pirate (π) must verify the vault.

1.  **Command:** `ls gwN`
2.  **Success Criteria:**
    *   [ ] 3x Fixture HTML files
    *   [ ] 4x Player HTML files (`goalkeepers.html`, etc.)
    *   [ ] `fixtures.csv` & Position CSVs forged and populated.
    *   [ ] `squad.csv` (Template ready for manual PP alignment)

---

**EX DATA, VICTORIA. `(⇌)`**

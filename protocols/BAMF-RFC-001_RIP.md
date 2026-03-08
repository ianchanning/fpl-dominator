# BAMF-RFC-001: THE RAPID INGESTION PROTOCOL (RIP) (v1.0)

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
*Estimated Time: 3 Minutes*

1.  **Login to FFS:** Access the [FFS Members area](https://members.fantasyfootballscout.co.uk/season-ticker/).
2.  **Navigate:** Go to the [Season Ticker](https://members.fantasyfootballscout.co.uk/season-ticker/).
3.  **Configure:** Select the next gameweek **GW(N+1)**.
4.  **The HTML Rip (via DevTools/Element Picker):**
    *   Find the `<div class="advanced-ticker" ...>` element.
    *   **Overall FDR:** Copy OuterHTML -> Save to `gwN/fixtures_5w.html`.
    *   **Defence FDR:** Copy OuterHTML -> Save to `gwN/fixtures_defence_5w.html`.
    *   **Attack FDR:** Copy OuterHTML -> Save to `gwN/fixtures_attack_5w.html`.
5.  **Execute Transformation:**
    *   **Command:** `bamf process-fixtures gwN`.
    *   *Verification:* Ensure `fixtures.csv` is populated.

---

## III. THE RITUAL OF THE SCROLL (FPL SCREENSHOTS)
*Estimated Time: 5 Minutes*

1.  **Login to FPL:** Access the [FPL Transfers Page](https://fantasy.premierleague.com/transfers).
2.  **Configure:** Change view to **'List View'**.
3.  **The Price Archive:** Screenshot of the full squad list (including headers) -> Save to `gwN/squad.png`.
4.  **The Position Archives (Zoom: 50% for full coverage):**
    *   **Goalkeepers:** Screenshot -> `gwN/goalkeepers.png`.
    *   **Defenders:** Screenshot P1 & P2 -> `gwN/defenders_1.png`, `gwN/defenders_2.png`.
    *   **Midfielders:** Screenshot P1 & P2 -> `gwN/midfielders_1.png`, `gwN/midfielders_2.png`.
    *   **Forwards:** Screenshot P1 & P2 -> `gwN/forwards_1.png`, `gwN/forwards_2.png`.

---

## IV. THE INTEGRITY CHECK (VERIFICATION)
Before the ritual is considered complete, the Carbon Pirate (π) must verify the vault.

1.  **Command:** `ls gwN`
2.  **Success Criteria:**
    *   [ ] 3x HTML files (Raw FDR Data)
    *   [ ] 1x `fixtures.csv` (Forged/Extracted)
    *   [ ] 7x PNG files (Raw Player/Squad Backup)
    *   [ ] `squad.csv` (Template ready for manual PP alignment)

---

**EX DATA, VICTORIA. `(⇌)`**

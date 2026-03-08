# BAMF-RFC-001: THE RAPID INGESTION PROTOCOL (RIP) (v1.3)

**Status:** APPROVED (Voyage Initialized) `(⇌)`
**Objective:** Reduce weekly data capture time to < 5 minutes.
**Core Philosophy:** Eliminate file-handling friction. **EX DATA, VICTORIA.**

---

## 0. SECURITY & THE VAULT OF SECRETS (MANDATORY)

- **The `.env` Sentinel:** All credentials reside in a local `.env` file (ignored by git).
- **Reference Keys:** `FPL_LOGIN`, `FPL_PASS`, `FFS_LOGIN`, `FFS_PASS`.

---

## I. PRE-FLIGHT: THE VAULT GENESIS
1.  **Command:** `bamf init gwN`
2.  **Outcome:** Sanctum created for the week's intelligence.

---

## II. THE RITUAL OF THE RIP (HIGH-SPEED INGESTION)
*Estimated Time: 3 Minutes*

This ritual uses the `bamf rip` command to bridge the browser clipboard directly to the vault.
**Note:** `bamf rip` automatically targets the most recently created `gwX` directory, as market data is ephemeral and tied to the live state.

### 2.1 Fixture Rips (FFS)
1.  Navigate to [FFS Season Ticker](https://members.fantasyfootballscout.co.uk/season-ticker/).
2.  Set Gameweek to **GW(N+1)**.
3.  **Overall FDR:** Copy OuterHTML -> `bamf rip fix`
4.  **Defence FDR:** Copy OuterHTML -> `bamf rip fix-d`
5.  **Attack FDR:**  Copy OuterHTML -> `bamf rip fix-a`

### 2.2 Player Rips (FPL)
1.  Navigate to [FPL Transfers](https://fantasy.premierleague.com/transfers) -> **List View**.
2.  **Goalkeepers:** Copy OuterHTML -> `bamf rip gkp`
3.  **Defenders:** 
    *   Page 1: Copy OuterHTML -> `bamf rip def`
    *   Page 2: Copy OuterHTML -> `bamf rip def2`
4.  **Midfielders:**
    *   Page 1: Copy OuterHTML -> `bamf rip mid`
    *   Page 2: Copy OuterHTML -> `bamf rip mid2`
5.  **Forwards:**
    *   Page 1: Copy OuterHTML -> `bamf rip fwd`
    *   Page 2: Copy OuterHTML -> `bamf rip fwd2`
6.  **Squad (Prices):** Copy OuterHTML -> `bamf rip squad`

---

## III. THE RITUAL OF FINALIZATION (THE SINGLE STRIKE)
*Estimated Time: 1 Minute*

With the raw HTML ripped into the vault, execute the end-to-end transformation.

1.  **Manual Bridge:** Open `gwN/squad.csv` and ensure your **Purchase Prices (PP)** are accurate.
2.  **Command:** `bamf finalize gwN`
3.  **Outcome:** The prophecy is forged, audited, and recorded to `gwN/squad_prophecy.md`.

---

## IV. THE INTEGRITY CHECK (VERIFICATION)
1.  **Command:** `ls gwN`
2.  **Success Criteria:**
    *   [ ] ~11 HTML files (The Ripped Evidence)
    *   [ ] 5x Position CSVs (The Extracted Reality)
    *   [ ] `fixtures.csv` (The Forged Schedule)
    *   [ ] `squad_prophecy.md` (The Final Vision)

---

**EX DATA, VICTORIA. `(⇌)`**

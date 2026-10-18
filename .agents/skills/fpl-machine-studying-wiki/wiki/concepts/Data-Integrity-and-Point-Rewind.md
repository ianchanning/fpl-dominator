---
title: Data Integrity and Point Rewind
category: Data Quality
tags: [data-cleaning, look-ahead-bias, recovery]
---

# Data Integrity and Point Rewind

### 1. The Sovereign Law
Maintain strict temporal isolation of gameweek data; if historical contamination occurs (look-ahead bias), recover by mapping the subsequent gameweek's single-week points (GWP) and subtracting them from the corrupted totals.

### 2. The Formulation & Trigger Context
This problem arises when data for gameweek $t+1$ is ingested into the vault for gameweek $t$. In FPL, total points (TP) are cumulative. If the "Total Points" column is ripped from a source after gameweek $t+1$ has occurred, the values in the $t$ vault are contaminated with points from $t+1$. This creates a "look-ahead bias" where the optimizer believes players were more productive in $t$ than they actually were, leading to incorrect strategic prophecies.

### 3. Dynamic Chaos vs. Typed Mathematical Truth

| Naive Approach (Dynamic Chaos) | Surgical Recovery (Mathematical Truth) |
| :--- | :--- |
| Manually editing CSV/HTML files based on memory. | Programmatic mapping of `Name` $\rightarrow$ `GWP` from a separate, verified GW(t+1) source. |
| Running subtraction scripts without a baseline. | Idempotent operations or strict single-execution protocols with pre-execution snapshots. |
| Assuming positional file alignment between vaults. | Name-based matching across all potential roster fragments (`_2.html`). |
| Ignoring the "look-ahead" as a minor noise. | Treating look-ahead bias as a critical integrity failure requiring total purification. |

### 4. The Pattern (❌ WRONG vs. ✅ RIGHT)

**❌ WRONG (Anti-Pattern): The Double-Rewind Loop**
Running a subtraction script multiple times on the same file without verifying the current state.
- **Symptom:** Players' total points plummet far below their actual historical values.
- **Result:** Data corruption that requires a full re-import of the vault.

**✅ RIGHT (Idiomatic Formulation): The Surgical Purge**

> [!IMPORTANT]
> A visual forensic record of this operation can be found in: `wiki/raw/visuals/point-rewind-visual.html`

1. **Harvest:** Scrape all `.html` files in the contaminated target's successor vault (GW8) to create a comprehensive mapping of `Player Name` to `Gameweek Points (GWP)`.
2. **Verify:** Match the name against the target vault (GW7) regardless of file position or order.
3. **Excise:** Perform the operation $\text{TP}_{\text{new}} = \text{TP}_{\text{current}} - \text{GWP}_{\text{successor}}$.
4. **Log:** Record every "Surgical Strike" to allow for auditability.

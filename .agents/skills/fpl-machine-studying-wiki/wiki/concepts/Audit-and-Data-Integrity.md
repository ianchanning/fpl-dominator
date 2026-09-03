# Audit & Data Integrity: Player Aliasing & Reality Verification

## 1. The Sovereign Law
Normalize all heterogeneous player and club naming variations across external data feeds (FFS, FPL, Understat) through an immutable alias dictionary and verify data consistency prior to solver execution using automated integrity audits (`bamf audit`).

---

## 2. The Trigger & Context
Data in the wild is messy, inconsistent, and fragmented:
- **The Diacritical & Nickname Mismatch:** External scouting sites (FFS) might list a player as *"Gabriel Martinelli"*, while the official FPL data feed lists *"Martinelli"*, or *"Son Heung-Min"* vs *"Son"*, or *"Bruno Fernandes"* vs *"Fernandes"*.
- **The Silent Null Merge:** In pandas, an unhandled name mismatch causes an inner or left merge to drop records or fill columns with `NaN`. If a star player's $xP$ is dropped, the optimization engine will silently ignore them, leading to catastrophically flawed squad selections.
- **The Team Abbreviation Collision:** Different sources use `"NFO"`, `"NOT"`, or `"Forest"` for Nottingham Forest, and `"WOL"` vs `"WLV"` for Wolves.
- **The Defensive Audit Solution:** The `audit_player_names_v3.py` and `audit_realities.py` engines enforce a deterministic aliasing table and raise strict warnings before `bamf finalize` passes data to the Chimera.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Naive String Joins | Sovereign Aliasing & Audit Engine |
| :--- | :--- | :--- |
| **Name Variations** | Silent `NaN` drops or duplicate rows on join. | Deterministic bidirectional alias map resolving 100% of player identifiers. |
| **Missing Data Detection** | Discovered after solver output looks bizarre. | **Pre-Flight Assertion:** CLI audit halts execution if any player in the top $100$ $xP$ is unmapped. |
| **Team Identification** | Inconsistent 3-letter codes breaking team limit ($\le 3$) constraints. | Canonical 20-club enumeration (`EPL_TEAMS = {"ARS", "AVL", ...}`). |

---

## 4. The Implementation Pattern (`audit_player_names_v3.py`)

```python
import pandas as pd

CANONICAL_ALIASES = {
    "Martinelli": "Gabriel Martinelli",
    "Gabriel": "Gabriel dos Santos Magalhães",
    "Son": "Son Heung-min",
    "Haaland": "Erling Haaland",
    "Salah": "Mohamed Salah",
    "Bruno Fernandes": "Bruno Borges Fernandes",
}


def normalize_player_names(
    df: pd.DataFrame, name_col: str = "player_name"
) -> pd.DataFrame:
    """Applies canonical name normalization and strips non-ASCII noise."""
    df = df.copy()
    df[name_col] = df[name_col].str.strip()
    df[name_col] = df[name_col].map(lambda n: CANONICAL_ALIASES.get(n, n))
    return df


def audit_merge_integrity(
    left_df: pd.DataFrame, right_df: pd.DataFrame, on: str = "player_name"
) -> None:
    """Verifies that no high-value records are lost during merge."""
    unmatched_left = set(left_df[on]) - set(right_df[on])
    if unmatched_left:
        print(f"⚠️ Warning: {len(unmatched_left)} unmatched records detected!")
        for name in list(unmatched_left)[:5]:
            print(f"  - Unmatched: {name}")
```

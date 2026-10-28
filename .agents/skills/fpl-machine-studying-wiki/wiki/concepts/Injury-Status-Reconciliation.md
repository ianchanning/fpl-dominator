# Injury Status Reconciliation (The Max-Severity Law)

## 1. The Sovereign Law

**A player's pool status is the MAX severity observed across any scraping source (OK < DOUBT < INJURY, commutative, never downgraded), and the solver pool excludes every `INJURY` row *after* reconciliation — an injured player must never reach the optimizer.**

## 2. Formulation & Trigger Context

RUD (gw9, 2026-10-28): the automated prophecy drafted **João Pedro** into the starting XI despite his injury. Forensics:

| Source | João Pedro | Saka |
| --- | --- | --- |
| `forwards.csv` / `midfielders.csv` (FPL market tables) | `Status=OK` | `Status=OK` |
| `squad.csv` (FPL squad page) | `Status=INJURY` | `Status=INJURY` |

Root cause: the market tables and the squad page are **independent scrapes** and can disagree (icon markup/timing). The legacy purge in `forge_cauldron` filtered `Status != "INJURY"` on the market file only — so it worked "correctly" and let him through. `update_prices.reconcile_timeline` — the stage that bends market reality to personal history — only reconciled **Price**, never Status.

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| ❌ WRONG (single-source trust) | ✅ RIGHT (lattice-join reconciliation) |
| --- | --- |
| Trust each scrape's `Status` at face value; purge on whichever file the pool is built from | Merge the squad page's Status into the pool by `(Surname, Position)`, keeping the **most severe** token per player |
| Ad-hoc `if squad says injured: delete row` | Typed severity ladder `{OK:0, DOUBT:1, INJURY:2}`; unknown tokens yield to known ones (a glitched value can never mask a real INJURY) |
| Downgrade market `INJURY` → squad `OK` because "the squad page is fresher" | Never downgrade: recovery news may be stale on *either* source; over-exclusion is the safe direction for an optimizer |
| Regenerate/mutate committed vault CSVs to "fix" history | Reconcile in the pool-builder; Layer-1 vault files stay byte-identical (tests enforce it) |

## 4. The Pattern

### ❌ WRONG (legacy `forge_cauldron`)

```python
enriched_df = pd.concat(df_list, ignore_index=True)
# market files only ever say "OK" -> nobody ever gets purged
enriched_df = enriched_df[enriched_df["Status"] != "INJURY"].copy()
```

### ✅ RIGHT (shipped fix, ~30 lines in `forge_cauldron.py`)

```python
_STATUS_SEVERITY = {"OK": 0, "DOUBT": 1, "INJURY": 2}

def _max_severity_status(pool_status: str, squad_status: str) -> str:
    pool_sev = _STATUS_SEVERITY.get(pool_status)
    squad_sev = _STATUS_SEVERITY.get(squad_status)
    if pool_sev is None:
        return squad_status          # glitched pool token yields to squad
    if squad_sev is None:
        return pool_status           # glitched squad token yields to pool
    return pool_status if pool_sev >= squad_sev else squad_status

# reconcile squad.csv (Surname, Position) -> pool, THEN purge INJURY
```

### Verification (Dan Luu battery — `tests/test_injury_reconciliation.py`, 17 tests)

- **Pure law:** 3×3 commutative/idempotent matrix + unknown-token masking cases.
- **Synthetic vaults:** squad-INJURY×market-OK (the João case), market-INJURY×squad-OK (no downgrade), DOUBT propagation (stays eligible), market-only INJURY (legacy law), squad member absent from market, no `squad.csv` (legacy path), PPM still computed.
- **Real-vault integration:** throwaway *copy* of `gw9` (Layer-1 immutability asserted via frame equality) — pool 240→238, João Pedro + Saka absent, zero INJURY rows in pool, Calafiori/Thomas upgraded to DOUBT but eligible, De Cuyper untouched.

## 5. Operational Notes

- Choke point: `forge_cauldron` runs first on **every** solver entry path (`finalize`, `run-gauntlet`), so reconciliation is universal; `update_prices` stays price-only (single responsibility).
- DOUBT is *not* purged by design (only `INJURY` excludes); DOUBT merely gets recorded in the pool status.
- The committed `gw9/squad_prophecy.md` (with João Pedro) is historical record — not regenerated; the fix protects future gameweeks and the test battery protects the law.
- Related: [[Automated-Data-Ingestion-and-Contract-Oracle]] (scrape sources), [[The-Chimera-Optimization-Engine]] (the consumer of the purified pool).
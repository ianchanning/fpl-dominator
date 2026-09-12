# Scenario Forge Analysis: GW3

**Total Scenarios Evaluated:** 3 (3 Successful)

## Temporal Stability Matrix

| Surname | Position | Team | Price | FLAT:1.00 | EXP:0.60 | EXP:0.20 | Robustness | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tzolakis | GKP | Hull City | 4.5 | [X] | [X] | [X] | 100% | IMMORTAL |
| Ajayi | DEF | Hull City | 4.1 | [X] | [X] | [X] | 100% | IMMORTAL |
| Tarkowski | DEF | Everton | 6.0 | [X]* | . | [X]* | 67% | FRINGE |
| Dedić | DEF | Newcastle | 4.5 | [X]* | [X]* | . | 67% | HORIZON-DEPENDENT |
| Calafiori | DEF | Arsenal | 5.6 | . | [X]* | . | 33% | FRINGE |
| Kayode | DEF | Brentford | 4.6 | . | . | [X]* | 33% | PURE PUNT |
| B.Fernandes | MID | Man Utd | 12.0 | [X] | [X] | [X] | 100% | IMMORTAL |
| Gakpo | MID | Liverpool | 7.0 | [X] | [X] | [X] | 100% | IMMORTAL |
| Saka | MID | Arsenal | 9.5 | [X]* | [X]* | . | 67% | HORIZON-DEPENDENT |
| Cherki | MID | Man City | 7.7 | . | [X]* | [X]* | 67% | PURE PUNT |
| Gibbs-White | MID | Nott'm Forest | 7.9 | . | . | [X]* | 33% | PURE PUNT |
| Dewsbury-Hall | MID | Everton | 6.5 | [X]* | . | . | 33% | HORIZON-DEPENDENT |
| Ndiaye | MID | Everton | 6.0 | [X]* | . | . | 33% | HORIZON-DEPENDENT |
| Stach | MID | Leeds | 6.0 | . | . | [X]* | 33% | PURE PUNT |
| Lewis-Potter | MID | Brentford | 5.5 | . | [X]* | . | 33% | FRINGE |
| Haaland | FWD | Man City | 15.5 | [X] | [X] | [X] | 100% | IMMORTAL |
| João Pedro | FWD | Chelsea | 7.6 | [X] | [X] | [X] | 100% | IMMORTAL |

*Legend:* `[X]` = Unanimous Starter | `[X]*` = Starting Alteration | `[b]` = Bench | `.` = Unselected

*Diff-First Noise Suppression:* Filtered 4 static bench players (Dovin, Egan, Obi, Thomas).

## Strategic Asset Classification

- **The Immortals (6 Locks):** Ajayi, B.Fernandes, Gakpo, Haaland, João Pedro, Tzolakis
- **The Horizon-Dependents (4 Assets):** Dedić, Dewsbury-Hall, Ndiaye, Saka
- **The Pure Punts (4 Assets):** Cherki, Gibbs-White, Kayode, Stach
- **The Fringe / Volatile (3 Assets):** Calafiori, Lewis-Potter, Tarkowski

## Weight Registry (Source of Truth)

```text
--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---
FLAT:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]
EXP:0.60   -> [1.00, 0.60, 0.36, 0.22, 0.13]
EXP:0.20   -> [1.00, 0.20, 0.04, 0.01, 0.00]
```

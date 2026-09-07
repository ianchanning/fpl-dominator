# Scenario Forge Analysis: GW4

**Total Scenarios Evaluated:** 5 (5 Successful)

## Temporal Stability Matrix

| Surname | Position | Team | Price | EXP:0.00 | EXP:0.25 | EXP:0.50 | EXP:0.75 | EXP:1.00 | Robustness | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tzolakis | GKP | Hull City | 4.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Ajayi | DEF | Hull City | 4.1 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Tarkowski | DEF | Everton | 6.0 | . | [X]* | [X]* | [X]* | [X]* | 80% | HORIZON-DEPENDENT |
| Hall | DEF | Newcastle | 5.1 | . | . | [X]* | [X]* | . | 40% | FRINGE |
| De Cuyper | DEF | Brighton | 4.7 | [X]* | [X]* | . | . | . | 40% | PURE PUNT |
| Calafiori | DEF | Arsenal | 5.7 | [X]* | . | . | . | . | 20% | PURE PUNT |
| Mendy | DEF | Hull City | 4.0 | [b] | [b] | [b] | [b] | [X]* | 20% | HORIZON-DEPENDENT |
| Davis | DEF | Ipswich Town | 4.0 | . | . | . | . | [b] | 0% | UNSELECTED |
| B.Fernandes | MID | Man Utd | 12.0 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Saka | MID | Arsenal | 9.5 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Gakpo | MID | Liverpool | 7.2 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Janelt | MID | Brentford | 5.0 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Ødegaard | MID | Arsenal | 6.6 | [X]* | [X]* | [X]* | [X]* | . | 80% | PURE PUNT |
| Mbeumo | MID | Man Utd | 7.9 | . | . | . | . | [X]* | 20% | HORIZON-DEPENDENT |
| Haaland | FWD | Man City | 15.5 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| João Pedro | FWD | Chelsea | 7.7 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Walle Egeli | FWD | Ipswich Town | 4.5 | [b] | [b] | . | . | . | 0% | UNSELECTED |
| Obi | FWD | Man Utd | 4.5 | . | . | [b] | [b] | [b] | 0% | UNSELECTED |

*Legend:* `[X]` = Unanimous Starter | `[X]*` = Starting Alteration | `[b]` = Bench | `.` = Unselected

*Diff-First Noise Suppression:* Filtered 2 static bench players (Steele, Thomas).

## Strategic Asset Classification

- **The Immortals (8 Locks):** Ajayi, B.Fernandes, Gakpo, Haaland, Janelt, João Pedro, Saka, Tzolakis
- **The Horizon-Dependents (3 Assets):** Mbeumo, Mendy, Tarkowski
- **The Pure Punts (3 Assets):** Calafiori, De Cuyper, Ødegaard
- **The Fringe / Volatile (1 Assets):** Hall

## Weight Registry (Source of Truth)

```text
--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---
EXP:0.00  -> [1.00, 0.00, 0.00, 0.00, 0.00]
EXP:0.25  -> [1.00, 0.25, 0.06, 0.02, 0.00]
EXP:0.50  -> [1.00, 0.50, 0.25, 0.12, 0.06]
EXP:0.75  -> [1.00, 0.75, 0.56, 0.42, 0.32]
EXP:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]
```

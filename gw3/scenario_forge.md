# Scenario Forge Analysis: GW3

**Total Scenarios Evaluated:** 5 (5 Successful)

## Temporal Stability Matrix

| Surname | Position | Team | Price | EXP:1.00 | EXP:0.75 | EXP:0.50 | EXP:0.25 | EXP:0.00 | Robustness | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tzolakis | GKP | Hull City | 4.5 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Dovin | GKP | Coventry City | 4.0 | [b] | [b] | [b] | . | [b] | 0% | UNSELECTED |
| Forster | GKP | Bournemouth | 4.0 | . | . | . | [b] | . | 0% | UNSELECTED |
| Calafiori | DEF | Arsenal | 5.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Ajayi | DEF | Hull City | 4.1 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Tarkowski | DEF | Everton | 6.0 | [X]* | [X]* | [X]* | . | . | 60% | HORIZON-DEPENDENT |
| Egan | DEF | Hull City | 4.0 | [b] | [b] | [X]* | [X]* | [X]* | 60% | PURE PUNT |
| Gabriel | DEF | Arsenal | 8.0 | [X]* | [X]* | . | . | . | 40% | HORIZON-DEPENDENT |
| Thomas | DEF | Coventry City | 4.0 | . | . | [b] | [b] | [b] | 0% | UNSELECTED |
| Davis | DEF | Ipswich Town | 4.0 | . | . | . | [b] | [b] | 0% | UNSELECTED |
| B.Fernandes | MID | Man Utd | 12.0 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Saka | MID | Arsenal | 9.5 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Cherki | MID | Man City | 7.7 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Stach | MID | Leeds | 6.0 | . | . | [X]* | [X]* | [X]* | 60% | PURE PUNT |
| Palmer | MID | Chelsea | 9.6 | [X]* | [X]* | . | . | . | 40% | HORIZON-DEPENDENT |
| Gibbs-White | MID | Nott'm Forest | 7.9 | [X]* | [X]* | . | . | . | 40% | HORIZON-DEPENDENT |
| Gakpo | MID | Liverpool | 7.0 | . | . | . | [X]* | [X]* | 40% | PURE PUNT |
| Yalcouyé | MID | Brighton | 4.5 | . | . | [b] | . | . | 0% | UNSELECTED |
| João Pedro | FWD | Chelsea | 7.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Haaland | FWD | Man City | 15.5 | . | . | [X]* | [X]* | [X]* | 60% | PURE PUNT |
| Walle Egeli | FWD | Ipswich Town | 4.5 | [b] | [b] | . | [b] | . | 0% | UNSELECTED |
| Obi | FWD | Man Utd | 4.5 | [b] | [b] | [b] | . | [b] | 0% | UNSELECTED |

*Legend:* `[X]` = Unanimous Starter | `[X]*` = Starting Alteration | `[b]` = Bench | `.` = Unselected

## Strategic Asset Classification

- **The Immortals (7 Locks):** Ajayi, B.Fernandes, Calafiori, Cherki, João Pedro, Saka, Tzolakis
- **The Horizon-Dependents (4 Assets):** Gabriel, Gibbs-White, Palmer, Tarkowski
- **The Pure Punts (4 Assets):** Egan, Gakpo, Haaland, Stach
- **The Fringe / Volatile (0 Assets):** None

## Weight Registry (Source of Truth)

```text
--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---
EXP:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]
EXP:0.75  -> [1.00, 0.75, 0.56, 0.42, 0.32]
EXP:0.50  -> [1.00, 0.50, 0.25, 0.12, 0.06]
EXP:0.25  -> [1.00, 0.25, 0.06, 0.02, 0.00]
EXP:0.00  -> [1.00, 0.00, 0.00, 0.00, 0.00]
```

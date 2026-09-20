# Scenario Forge Analysis: GW6

**Total Scenarios Evaluated:** 5 (5 Successful)

## Temporal Stability Matrix

| Surname | Position | Team | Price | EXP:0.00 | EXP:0.25 | EXP:0.50 | EXP:0.75 | EXP:1.00 | Robustness | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tzolakis | GKP | Hull City | 4.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Tarkowski | DEF | Everton | 6.1 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Bogle | DEF | Leeds | 4.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| De Cuyper | DEF | Brighton | 4.9 | [X]* | [X]* | [X]* | [X]* | . | 80% | PURE PUNT |
| Vuskovic | DEF | Brighton | 5.0 | [X]* | [X]* | [X]* | . | . | 60% | PURE PUNT |
| Gvardiol | DEF | Man City | 5.7 | . | . | . | [X]* | . | 20% | FRINGE |
| Hall | DEF | Newcastle | 5.2 | . | . | . | . | [X]* | 20% | HORIZON-DEPENDENT |
| Davis | DEF | Ipswich Town | 4.0 | . | . | . | . | [b] | 0% | UNSELECTED |
| B.Fernandes | MID | Man Utd | 12.0 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Groß | MID | Brighton | 5.8 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| Schade | MID | Brentford | 6.1 | [X]* | . | [X]* | [X]* | [X]* | 80% | FRINGE |
| Saka | MID | Arsenal | 9.5 | . | . | [X]* | [X]* | [X]* | 60% | HORIZON-DEPENDENT |
| Tavernier | MID | Bournemouth | 6.1 | [X]* | [X]* | . | . | [X]* | 60% | FRINGE |
| Scott | MID | Bournemouth | 6.1 | [X]* | [X]* | . | . | . | 40% | PURE PUNT |
| Belloumi | MID | Hull City | 5.1 | . | [X]* | [X]* | . | . | 40% | FRINGE |
| Yalcouyé | MID | Brighton | 4.5 | . | . | . | [b] | . | 0% | UNSELECTED |
| Haaland | FWD | Man City | 15.6 | [X] | [X] | [X] | [X] | [X] | 100% | IMMORTAL |
| João Pedro | FWD | Chelsea | 7.8 | . | . | . | [X]* | [X]* | 40% | HORIZON-DEPENDENT |
| Walle Egeli | FWD | Ipswich Town | 4.5 | [b] | [b] | [b] | . | . | 0% | UNSELECTED |

*Legend:* `[X]` = Unanimous Starter | `[X]*` = Starting Alteration | `[b]` = Bench | `.` = Unselected

*Diff-First Noise Suppression:* Filtered 3 static bench players (Balcombe, Giles, Salia).

## Strategic Asset Classification

- **The Immortals (6 Locks):** B.Fernandes, Bogle, Groß, Haaland, Tarkowski, Tzolakis
- **The Horizon-Dependents (3 Assets):** Hall, João Pedro, Saka
- **The Pure Punts (3 Assets):** De Cuyper, Scott, Vuskovic
- **The Fringe / Volatile (4 Assets):** Belloumi, Gvardiol, Schade, Tavernier

## Weight Registry (Source of Truth)

```text
--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---
EXP:0.00  -> [1.00, 0.00, 0.00, 0.00, 0.00]
EXP:0.25  -> [1.00, 0.25, 0.06, 0.02, 0.00]
EXP:0.50  -> [1.00, 0.50, 0.25, 0.12, 0.06]
EXP:0.75  -> [1.00, 0.75, 0.56, 0.42, 0.32]
EXP:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]
```

# Scenario Forge Analysis: GW3

**Total Scenarios Evaluated:** 3 (3 Successful)

## Temporal Stability Matrix

| Surname | Position | Team | Price | FLAT:1.00 | EXP:0.60 | EXP:0.20 | Robustness | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Horníček | GKP | Newcastle | 5.0 | . | [X]* | . | 33% | FRINGE |
| Kelleher | GKP | Brentford | 5.0 | . | . | [X]* | 33% | PURE PUNT |
| Tzolakis | GKP | Hull City | 4.5 | [X]* | . | . | 33% | HORIZON-DEPENDENT |
| Hall | DEF | Newcastle | 5.0 | [X]* | [X]* | . | 67% | HORIZON-DEPENDENT |
| Dedić | DEF | Newcastle | 4.5 | [X]* | [X]* | . | 67% | HORIZON-DEPENDENT |
| Ajayi | DEF | Hull City | 4.1 | . | [X]* | [X]* | 67% | PURE PUNT |
| Collins | DEF | Brentford | 5.5 | . | . | [X]* | 33% | PURE PUNT |
| Thiaw | DEF | Newcastle | 5.0 | [X]* | . | . | 33% | HORIZON-DEPENDENT |
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

*Diff-First Noise Suppression:* Filtered 4 static bench players (Dovin, Egan, Mendy, Obi).

## Strategic Asset Classification

- **The Immortals (4 Locks):** B.Fernandes, Gakpo, Haaland, João Pedro
- **The Horizon-Dependents (7 Assets):** Dedić, Dewsbury-Hall, Hall, Ndiaye, Saka, Thiaw, Tzolakis
- **The Pure Punts (7 Assets):** Ajayi, Cherki, Collins, Gibbs-White, Kayode, Kelleher, Stach
- **The Fringe / Volatile (2 Assets):** Horníček, Lewis-Potter

## Weight Registry (Source of Truth)

```text
--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---
FLAT:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]
EXP:0.60   -> [1.00, 0.60, 0.36, 0.22, 0.13]
EXP:0.20   -> [1.00, 0.20, 0.04, 0.01, 0.00]
```

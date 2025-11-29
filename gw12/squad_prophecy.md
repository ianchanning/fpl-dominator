# FPL Dominator Squad Prophecy for GW12

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw12/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score
   Roefs     Sunderland      GKP    4.7         0.05
   Muñoz Crystal Palace      DEF    5.9         0.06
J.Timber        Arsenal      DEF    6.3         0.06
   Guéhi Crystal Palace      DEF    5.1         0.06
 Lacroix Crystal Palace      DEF    5.0         0.06
 Semenyo    Bournemouth      MID    7.9         0.07
    Rice        Arsenal      MID    6.9         0.07
  Mbeumo        Man Utd      MID    8.6         0.06
  Cullen        Burnley      MID    5.0         0.05
 Haaland       Man City      FWD   14.9         0.10
  Thiago      Brentford      FWD    6.5         0.06

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname    Team Position  Price  Final_Score
  Setford Arsenal      GKP    4.0         0.00
   Estève Burnley      DEF    3.9         0.03
    Stach   Leeds      MID    4.8         0.04
Marc Guiu Chelsea      FWD    4.2         0.01

-------------------------------------------
Total Squad Cost:          £93.7m
Projected Starting Score:    0.70
Money in the Bank:         £6.3m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Intelligence loaded. Analyzing 198 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1250).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Roefs     Sunderland      GKP    4.7         0.05                     1252.8
   Muñoz Crystal Palace      DEF    5.9         0.06                     1184.6
J.Timber        Arsenal      DEF    6.3         0.06                     1173.8
   Guéhi Crystal Palace      DEF    5.1         0.06                     1184.6
 Lacroix Crystal Palace      DEF    5.0         0.06                     1184.6
 Semenyo    Bournemouth      MID    7.9         0.07                     1126.8
    Rice        Arsenal      MID    6.9         0.07                     1145.0
  Mbeumo        Man Utd      MID    8.6         0.06                     1121.8
 Caicedo        Chelsea      MID    6.1         0.05                     1196.2
 Haaland       Man City      FWD   14.9         0.10                     1124.0
  Thiago      Brentford      FWD    6.5         0.06                     1145.8

--- BENCH (Potency & Cost Optimized) ---
  Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Dúbravka Burnley      GKP    4.0         0.03                     1188.2
   Estève Burnley      DEF    3.9         0.03                     1188.2
    Stach   Leeds      MID    4.8         0.04                     1177.8
Marc Guiu Chelsea      FWD    4.2         0.01                     1196.2

-------------------------------------------
Total Squad Cost:          £94.8m
Projected Starting Score:    0.70
Money in the Bank:         £5.2m
-------------------------------------------

```

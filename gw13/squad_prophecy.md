# FPL Dominator Squad Prophecy for GW13

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw13/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score
    Raya        Arsenal      GKP    5.9     0.051408
 Gabriel        Arsenal      DEF    6.3     0.103240
   Muñoz Crystal Palace      DEF    6.0     0.070473
 Lacroix Crystal Palace      DEF    5.1     0.065774
Chalobah        Chelsea      DEF    5.2     0.065530
    Rice        Arsenal      MID    7.0     0.074126
   Kudus          Spurs      MID    6.5     0.071439
 Semenyo    Bournemouth      MID    7.8     0.069563
   Foden       Man City      MID    8.1     0.064810
 Haaland       Man City      FWD   14.9     0.109345
  Thiago      Brentford      FWD    6.7     0.074424

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname        Team Position  Price  Final_Score
 Dúbravka     Burnley      GKP    4.0     0.033380
   Estève     Burnley      DEF    3.9     0.031268
 P.M.Sarr       Spurs      MID    4.8     0.034325
Kroupi.Jr Bournemouth      FWD    4.6     0.030379

-------------------------------------------
Total Squad Cost:          £96.8m
Projected Starting Score:    0.82
Money in the Bank:         £3.2m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 162 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1175).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Raya        Arsenal      GKP    5.9     0.051408                1176.866667
Gabriel        Arsenal      DEF    6.3     0.103240                1176.866667
  Muñoz Crystal Palace      DEF    6.0     0.070473                1170.666667
Lacroix Crystal Palace      DEF    5.1     0.065774                1170.666667
   Rice        Arsenal      MID    7.0     0.074126                1133.200000
  Kudus          Spurs      MID    6.5     0.071439                1165.333333
Semenyo    Bournemouth      MID    7.8     0.069563                1135.666667
  Foden       Man City      MID    8.1     0.064810                1141.800000
  Gakpo      Liverpool      MID    7.5     0.064563                1122.933333
Haaland       Man City      FWD   14.9     0.109345                1141.800000
 Thiago      Brentford      FWD    6.7     0.074424                1216.000000

--- BENCH (Potency & Cost Optimized) ---
  Surname        Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Dúbravka     Burnley      GKP    4.0     0.033380                1183.333333
  Hartman     Burnley      DEF    4.0     0.036761                1183.333333
   Estève     Burnley      DEF    3.9     0.031268                1183.333333
Kroupi.Jr Bournemouth      FWD    4.6     0.030379                1135.666667

-------------------------------------------
Total Squad Cost:          £98.3m
Projected Starting Score:    0.82
Money in the Bank:         £1.7m
-------------------------------------------

```

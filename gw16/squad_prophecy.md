# FPL Dominator Squad Prophecy for GW16

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw16/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score
      Roefs     Sunderland      GKP    4.8     0.067273
      Guéhi Crystal Palace      DEF    4.6     0.131729
      Rúben       Man City      DEF    5.6     0.077961
      Keane        Everton      DEF    4.6     0.071214
B.Fernandes        Man Utd      MID    9.1     0.102288
      Foden       Man City      MID    8.2     0.096348
    Semenyo    Bournemouth      MID    7.4     0.089451
     Wilson         Fulham      MID    5.6     0.089060
    Caicedo        Chelsea      MID    5.7     0.083498
    Haaland       Man City      FWD   14.1     0.150061
     Thiago      Brentford      FWD    6.5     0.081716

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname       Team Position  Price  Final_Score
   Darlow      Leeds      GKP    3.9     0.008210
 Reinildo Sunderland      DEF    3.9     0.052893
  Hartman    Burnley      DEF    4.0     0.043043
Marc Guiu    Chelsea      FWD    4.2     0.010162

-------------------------------------------
Total Squad Cost:          £92.2m
Projected Starting Score:    1.04
Money in the Bank:         £7.8m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 152 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1150).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Roefs     Sunderland      GKP    4.8     0.067273                1189.190045
   Guéhi Crystal Palace      DEF    4.6     0.131729                1187.285068
   Rúben       Man City      DEF    5.6     0.077961                1159.552036
Andersen         Fulham      DEF    4.6     0.050721                1145.479638
   Foden       Man City      MID    8.2     0.096348                1101.217195
 Semenyo    Bournemouth      MID    7.4     0.089451                1093.339367
  Wilson         Fulham      MID    5.6     0.089060                1114.977376
    Rice        Arsenal      MID    6.9     0.080756                1149.144796
 Haaland       Man City      FWD   14.1     0.150061                1101.217195
  Thiago      Brentford      FWD    6.5     0.081716                1098.923077
   Bowen       West Ham      FWD    7.5     0.079040                1143.719457

--- BENCH (Potency & Cost Optimized) ---
 Surname       Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Darlow      Leeds      GKP    3.9     0.008210                1218.085973
Reinildo Sunderland      DEF    3.9     0.052893                1189.190045
 Hartman    Burnley      DEF    4.0     0.043043                1168.601810
E Le Fee Sunderland      MID    4.9     0.053522                1135.990950

-------------------------------------------
Total Squad Cost:          £92.5m
Projected Starting Score:    0.99
Money in the Bank:         £7.5m
-------------------------------------------

```

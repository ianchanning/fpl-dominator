# FPL Dominator Squad Prophecy for GW11

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw11/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
   Surname           Team Position  Price  Final_Score
     Roefs     Sunderland      GKP    4.7         0.05
  J.Timber        Arsenal      DEF    5.6         0.06
     Guehi Crystal Palace      DEF    4.6         0.06
 Calafiori        Arsenal      DEF    5.8         0.06
  Chalobah        Chelsea      DEF    5.1         0.06
   M.Salah      Liverpool      MID   14.5         0.08
   Semenyo    Bournemouth      MID    7.4         0.07
      Rice        Arsenal      MID    6.9         0.06
   Haaland       Man City      FWD   14.1         0.14
    Thiago      Brentford      FWD    6.3         0.06
João Pedro        Chelsea      FWD    7.7         0.06

--- BENCH (RUTHLESSLY Cost-Optimized) ---
   Surname    Team Position  Price  Final_Score
  Dúbravka Burnley      GKP    4.0         0.03
Acheampong Chelsea      DEF    3.9         0.02
      King   Spurs      MID    4.5         0.02
  P.M.Sarr   Spurs      MID    4.8         0.03

-------------------------------------------
Total Squad Cost:          £99.9m
Projected Starting Score:    0.76
Money in the Bank:         £0.1m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Intelligence loaded. Analyzing 180 players.
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
     Roefs     Sunderland      GKP    4.7         0.05                     1180.0
  J.Timber        Arsenal      DEF    5.6         0.06                     1140.0
     Guehi Crystal Palace      DEF    4.6         0.06                     1100.0
 Calafiori        Arsenal      DEF    5.8         0.06                     1140.0
  Chalobah        Chelsea      DEF    5.1         0.06                     1140.0
   M.Salah      Liverpool      MID   14.5         0.08                     1080.0
   Semenyo    Bournemouth      MID    7.4         0.07                     1080.0
      Rice        Arsenal      MID    6.9         0.06                     1140.0
   Haaland       Man City      FWD   14.1         0.14                     1120.0
    Thiago      Brentford      FWD    6.3         0.06                     1140.0
João Pedro        Chelsea      FWD    7.7         0.06                     1140.0

--- BENCH (Potency & Cost Optimized) ---
   Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Dúbravka Burnley      GKP    4.0         0.03                     1160.0
Acheampong Chelsea      DEF    3.9         0.02                     1140.0
  P.M.Sarr   Spurs      MID    4.8         0.03                     1160.0
      King   Spurs      MID    4.5         0.02                     1160.0

-------------------------------------------
Total Squad Cost:          £99.9m
Projected Starting Score:    0.76
Money in the Bank:         £0.1m
-------------------------------------------

```

# FPL Dominator Squad Prophecy for GW12

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw12/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
  Surname           Team Position  Price  Final_Score
    Roefs     Sunderland      GKP    4.7         0.06
 Chalobah        Chelsea      DEF    5.1         0.09
    Muñoz Crystal Palace      DEF    5.9         0.08
Calafiori        Arsenal      DEF    5.8         0.08
    Keane        Everton      DEF    4.5         0.07
  M.Salah      Liverpool      MID   14.2         0.09
  Semenyo    Bournemouth      MID    7.9         0.08
     Rice        Arsenal      MID    6.9         0.08
 Bruno G.      Newcastle      MID    6.6         0.08
  Haaland       Man City      FWD   14.9         0.16
   Thiago      Brentford      FWD    6.5         0.08

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname    Team Position  Price  Final_Score
   Darlow   Leeds      GKP    4.0         0.01
   Estève Burnley      DEF    3.9         0.03
 P.M.Sarr   Spurs      MID    4.8         0.04
Marc Guiu Chelsea      FWD    4.2         0.01

-------------------------------------------
Total Squad Cost:          £99.9m
Projected Starting Score:    0.95
Money in the Bank:         £0.1m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 197 players.
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
    Roefs     Sunderland      GKP    4.7         0.06                     1252.8
 Chalobah        Chelsea      DEF    5.1         0.09                     1189.0
    Muñoz Crystal Palace      DEF    5.9         0.08                     1184.6
Calafiori        Arsenal      DEF    5.8         0.08                     1173.8
    Keane        Everton      DEF    4.5         0.07                     1184.6
  M.Salah      Liverpool      MID   14.2         0.09                     1117.2
  Semenyo    Bournemouth      MID    7.9         0.08                     1126.8
     Rice        Arsenal      MID    6.9         0.08                     1145.0
 Bruno G.      Newcastle      MID    6.6         0.08                     1126.2
  Haaland       Man City      FWD   14.9         0.16                     1124.0
   Thiago      Brentford      FWD    6.5         0.08                     1145.8

--- BENCH (Potency & Cost Optimized) ---
  Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Dúbravka Burnley      GKP    4.0         0.04                     1188.2
   Estève Burnley      DEF    3.9         0.03                     1188.2
 P.M.Sarr   Spurs      MID    4.8         0.04                     1150.2
Marc Guiu Chelsea      FWD    4.2         0.01                     1196.2

-------------------------------------------
Total Squad Cost:          £99.9m
Projected Starting Score:    0.95
Money in the Bank:         £0.1m
-------------------------------------------

```

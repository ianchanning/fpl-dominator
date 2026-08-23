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
     Pickford        Everton      GKP    5.5     0.051268
        Guéhi Crystal Palace      DEF    5.1     0.088025
        Muñoz Crystal Palace      DEF    5.9     0.071441
        Keane        Everton      DEF    4.5     0.065251
      Lacroix Crystal Palace      DEF    5.0     0.064212
         Rice        Arsenal      MID    6.9     0.068426
      Semenyo    Bournemouth      MID    7.9     0.067796
      M.Salah      Liverpool      MID   14.2     0.063469
Dewsbury-Hall        Everton      MID    4.9     0.061647
      Haaland       Man City      FWD   14.9     0.109548
       Thiago      Brentford      FWD    6.5     0.066853

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname    Team Position  Price  Final_Score
  Setford Arsenal      GKP    4.0     0.000000
   Estève Burnley      DEF    3.9     0.028487
 P.M.Sarr   Spurs      MID    4.8     0.034637
Marc Guiu Chelsea      FWD    4.2     0.013617

-------------------------------------------
Total Squad Cost:          £98.2m
Projected Starting Score:    0.78
Money in the Bank:         £1.8m
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
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1150).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
   Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Pickford        Everton      GKP    5.5     0.051268                1180.066667
     Guéhi Crystal Palace      DEF    5.1     0.088025                1175.800000
     Muñoz Crystal Palace      DEF    5.9     0.071441                1175.800000
     Rúben       Man City      DEF    5.5     0.051089                1145.066667
   Semenyo    Bournemouth      MID    7.9     0.067796                1143.133333
   M.Salah      Liverpool      MID   14.2     0.063469                1100.533333
    Minteh       Brighton      MID    6.2     0.059715                1138.733333
  Bruno G.      Newcastle      MID    6.6     0.059548                1125.133333
J.Palhinha          Spurs      MID    5.5     0.056559                1140.400000
   Haaland       Man City      FWD   14.9     0.109548                1128.733333
   Welbeck       Brighton      FWD    6.6     0.055325                1138.733333

--- BENCH (Potency & Cost Optimized) ---
  Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Dúbravka Burnley      GKP    4.0     0.032676                1193.533333
  Hartman Burnley      DEF    4.0     0.047757                1193.533333
   Estève Burnley      DEF    3.9     0.028487                1193.533333
Marc Guiu Chelsea      FWD    4.2     0.013617                1211.733333

-------------------------------------------
Total Squad Cost:          £100.0m
Projected Starting Score:    0.73
Money in the Bank:         £0.0m
-------------------------------------------

```

# FPL Dominator Squad Prophecy for GW29

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw29/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score
  Henderson Crystal Palace      GKP    5.0     0.189911
    Gabriel        Arsenal      DEF    6.6     0.265379
   J.Timber        Arsenal      DEF    6.4     0.239489
      Guéhi       Man City      DEF    4.6     0.221832
    Semenyo       Man City      MID    7.4     0.285693
       Rice        Arsenal      MID    6.9     0.268507
B.Fernandes        Man Utd      MID    9.5     0.235981
     Wilson         Fulham      MID    6.0     0.211404
    Haaland       Man City      FWD   14.1     0.349056
 João Pedro        Chelsea      FWD    7.7     0.224493
     Thiago      Brentford      FWD    6.5     0.208638

--- BENCH (RUTHLESSLY Cost-Optimized) ---
Surname     Team Position  Price  Final_Score
 Darlow    Leeds      GKP    3.9     0.043404
  Rodon    Leeds      DEF    3.9     0.122979
  Diouf West Ham      DEF    4.0     0.110505
  Stach    Leeds      MID    4.7     0.165306

-------------------------------------------
Total Squad Cost:          £97.2m
Projected Starting Score:    2.70
Money in the Bank:         £2.8m
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
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 5 starters with FDR > 1290).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Henderson Crystal Palace      GKP    5.0     0.189911                1029.428571
    Gabriel        Arsenal      DEF    6.6     0.265379                1050.571429
   J.Timber        Arsenal      DEF    6.4     0.239489                1050.571429
      Guéhi       Man City      DEF    4.6     0.221832                1019.238095
    Semenyo       Man City      MID    7.4     0.285693                1023.476190
       Rice        Arsenal      MID    6.9     0.268507                1027.904762
B.Fernandes        Man Utd      MID    9.5     0.235981                1195.857143
     Wilson         Fulham      MID    6.0     0.211404                1147.095238
    Haaland       Man City      FWD   14.1     0.349056                1023.476190
 João Pedro        Chelsea      FWD    7.7     0.224493                1211.619048
     Thiago      Brentford      FWD    6.5     0.208638                1189.142857

--- BENCH (Potency & Cost Optimized) ---
Surname     Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Darlow    Leeds      GKP    3.9     0.043404                1175.000000
  Rodon    Leeds      DEF    3.9     0.122979                1175.000000
  Diouf West Ham      DEF    4.0     0.110505                1215.333333
  Stach    Leeds      MID    4.7     0.165306                1196.571429

-------------------------------------------
Total Squad Cost:          £97.2m
Projected Starting Score:    2.70
Money in the Bank:         £2.8m
-------------------------------------------

```

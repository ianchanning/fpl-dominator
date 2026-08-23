# FPL Dominator Squad Prophecy for GW26

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw26/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score
      Roefs     Sunderland      GKP    4.9     0.149688
    Gabriel        Arsenal      DEF    7.1     0.207839
      Guéhi       Man City      DEF    5.2     0.183373
    Lacroix Crystal Palace      DEF    5.1     0.176597
    Semenyo       Man City      MID    8.0     0.228358
       Rice        Arsenal      MID    7.6     0.223464
B.Fernandes        Man Utd      MID    9.8     0.202415
     Wilson         Fulham      MID    6.0     0.174588
    Haaland       Man City      FWD   14.9     0.301010
 João Pedro        Chelsea      FWD    7.7     0.194110
     Thiago      Brentford      FWD    7.0     0.193621

--- BENCH (RUTHLESSLY Cost-Optimized) ---
Surname        Team Position  Price  Final_Score
 Darlow       Leeds      GKP    3.9     0.032034
  Rodon       Leeds      DEF    3.9     0.107245
   Hill Bournemouth      DEF    4.0     0.084495
  Stach       Leeds      MID    4.7     0.139389

-------------------------------------------
Total Squad Cost:          £99.8m
Projected Starting Score:    2.24
Money in the Bank:         £0.2m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 184 players.
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
      Roefs     Sunderland      GKP    4.9     0.149688                1215.190476
    Gabriel        Arsenal      DEF    7.1     0.207839                1161.476190
      Guéhi       Man City      DEF    5.2     0.183373                1149.571429
    Lacroix Crystal Palace      DEF    5.1     0.176597                1116.666667
    Semenyo       Man City      MID    8.0     0.228358                1139.000000
       Rice        Arsenal      MID    7.6     0.223464                1143.809524
B.Fernandes        Man Utd      MID    9.8     0.202415                1201.000000
     Wilson         Fulham      MID    6.0     0.174588                1194.238095
    Haaland       Man City      FWD   14.9     0.301010                1139.000000
 João Pedro        Chelsea      FWD    7.7     0.194110                1156.047619
     Thiago      Brentford      FWD    7.0     0.193621                1193.571429

--- BENCH (Potency & Cost Optimized) ---
Surname        Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Darlow       Leeds      GKP    3.9     0.032034                1220.571429
  Rodon       Leeds      DEF    3.9     0.107245                1220.571429
   Hill Bournemouth      DEF    4.0     0.084495                1187.047619
  Stach       Leeds      MID    4.7     0.139389                1211.714286

-------------------------------------------
Total Squad Cost:          £99.8m
Projected Starting Score:    2.24
Money in the Bank:         £0.2m
-------------------------------------------

```

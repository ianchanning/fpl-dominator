# FPL Dominator Squad Prophecy for GW19

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw19/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
  Surname        Team Position  Price  Final_Score
 Pickford     Everton      GKP    5.5     0.083252
   Romero       Spurs      DEF    5.0     0.100365
Tarkowski     Everton      DEF    5.6     0.090704
 J.Timber     Arsenal      DEF    5.6     0.087099
   Minteh    Brighton      MID    6.0     0.120998
Tavernier Bournemouth      MID    5.6     0.113967
    Kudus       Spurs      MID    6.4     0.111714
  Semenyo Bournemouth      MID    7.4     0.103817
 Grealish     Everton      MID    6.5     0.102006
  Haaland    Man City      FWD   14.1     0.150972
   Thiago   Brentford      FWD    6.5     0.087460

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname     Team Position  Price  Final_Score
     Darlow    Leeds      GKP    3.9     0.008440
Gudmundsson    Leeds      DEF    3.8     0.068071
      Diouf West Ham      DEF    4.0     0.064964
  Marc Guiu  Chelsea      FWD    4.2     0.010303

-------------------------------------------
Total Squad Cost:          £90.1m
Projected Starting Score:    1.15
Money in the Bank:         £9.9m
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
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1170).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
  Surname        Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Pickford     Everton      GKP    5.5     0.083252                1167.533333
   Romero       Spurs      DEF    5.0     0.100365                1151.800000
Tarkowski     Everton      DEF    5.6     0.090704                1167.533333
 J.Timber     Arsenal      DEF    5.6     0.087099                1211.266667
   Minteh    Brighton      MID    6.0     0.120998                1109.933333
Tavernier Bournemouth      MID    5.6     0.113967                1206.933333
    Kudus       Spurs      MID    6.4     0.111714                1132.800000
  Semenyo Bournemouth      MID    7.4     0.103817                1206.933333
 Grealish     Everton      MID    6.5     0.102006                1116.600000
  Haaland    Man City      FWD   14.1     0.150972                1141.600000
   Thiago   Brentford      FWD    6.5     0.087460                1153.666667

--- BENCH (Potency & Cost Optimized) ---
    Surname     Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
     Darlow    Leeds      GKP    3.9     0.008440                1184.800000
Gudmundsson    Leeds      DEF    3.8     0.068071                1184.800000
      Diouf West Ham      DEF    4.0     0.064964                1151.400000
  Marc Guiu  Chelsea      FWD    4.2     0.010303                1164.666667

-------------------------------------------
Total Squad Cost:          £90.1m
Projected Starting Score:    1.15
Money in the Bank:         £9.9m
-------------------------------------------

```

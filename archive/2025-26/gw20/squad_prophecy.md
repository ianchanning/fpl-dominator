# FPL Dominator Squad Prophecy for GW20

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw20/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
  Surname        Team Position  Price  Final_Score
     Pope   Newcastle      GKP    5.1     0.091492
  Gabriel     Arsenal      DEF    6.6     0.149139
 Chalobah     Chelsea      DEF    5.3     0.143593
Tarkowski     Everton      DEF    5.6     0.096590
     Rice     Arsenal      MID    6.9     0.126874
    Stach       Leeds      MID    4.9     0.126369
Tavernier Bournemouth      MID    5.6     0.122793
 Casemiro     Man Utd      MID    5.5     0.118280
   Schade   Brentford      MID    7.1     0.118237
  Haaland    Man City      FWD   14.1     0.171455
   Thiago   Brentford      FWD    6.5     0.113397

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname     Team Position  Price  Final_Score
     Darlow    Leeds      GKP    3.9     0.008521
Gudmundsson    Leeds      DEF    3.8     0.071621
      Diouf West Ham      DEF    4.0     0.064840
  Marc Guiu  Chelsea      FWD    4.2     0.010560

-------------------------------------------
Total Squad Cost:          £89.1m
Projected Starting Score:    1.38
Money in the Bank:         £10.9m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 157 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1190).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
  Surname        Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
     Pope   Newcastle      GKP    5.1     0.091492                1170.600000
  Gabriel     Arsenal      DEF    6.6     0.149139                1208.266667
 Chalobah     Chelsea      DEF    5.3     0.143593                1172.066667
Tarkowski     Everton      DEF    5.6     0.096590                1153.333333
     Rice     Arsenal      MID    6.9     0.126874                1151.533333
    Stach       Leeds      MID    4.9     0.126369                1175.133333
Tavernier Bournemouth      MID    5.6     0.122793                1147.866667
 Casemiro     Man Utd      MID    5.5     0.118280                1192.933333
   Schade   Brentford      MID    7.1     0.118237                1157.000000
  Haaland    Man City      FWD   14.1     0.171455                1133.533333
   Thiago   Brentford      FWD    6.5     0.113397                1157.000000

--- BENCH (Potency & Cost Optimized) ---
    Surname     Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
     Darlow    Leeds      GKP    3.9     0.008521                1173.533333
Gudmundsson    Leeds      DEF    3.8     0.071621                1173.533333
      Diouf West Ham      DEF    4.0     0.064840                1153.600000
  Marc Guiu  Chelsea      FWD    4.2     0.010560                1136.400000

-------------------------------------------
Total Squad Cost:          £89.1m
Projected Starting Score:    1.38
Money in the Bank:         £10.9m
-------------------------------------------

```

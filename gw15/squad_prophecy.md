# FPL Dominator Squad Prophecy for GW15

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw15/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score
       Raya        Arsenal      GKP    6.0     0.098047
     Senesi    Bournemouth      DEF    5.0     0.102004
      Guehi Crystal Palace      DEF    5.2     0.087140
      Muñoz Crystal Palace      DEF    6.1     0.080915
      Stach          Leeds      MID    4.8     0.094731
      Foden       Man City      MID    8.6     0.087778
B.Fernandes        Man Utd      MID    9.0     0.086686
       Rice        Arsenal      MID    7.1     0.085498
    Semenyo    Bournemouth      MID    7.6     0.080887
    Haaland       Man City      FWD   15.0     0.134053
     Thiago      Brentford      FWD    6.9     0.079929

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname       Team Position  Price  Final_Score
   Darlow      Leeds      GKP    3.9     0.008297
   Estève    Burnley      DEF    3.9     0.039990
 Alderete Sunderland      DEF    4.0     0.045221
Marc Guiu    Chelsea      FWD    4.2     0.017528

-------------------------------------------
Total Squad Cost:          £97.3m
Projected Starting Score:    1.02
Money in the Bank:         £2.7m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 187 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 2 starters with FDR > 1160).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
       Raya        Arsenal      GKP    6.0     0.098047                1144.348416
     Senesi    Bournemouth      DEF    5.0     0.102004                1183.289593
      Guehi Crystal Palace      DEF    5.2     0.087140                1221.027149
   Chalobah        Chelsea      DEF    5.3     0.077954                1159.651584
      Stach          Leeds      MID    4.8     0.094731                1154.850679
      Foden       Man City      MID    8.6     0.087778                1131.266968
B.Fernandes        Man Utd      MID    9.0     0.086686                1158.199095
       Rice        Arsenal      MID    7.1     0.085498                1102.945701
    Semenyo    Bournemouth      MID    7.6     0.080887                1117.615385
    Haaland       Man City      FWD   15.0     0.134053                1131.266968
     Thiago      Brentford      FWD    6.9     0.079929                1089.719457

--- BENCH (Potency & Cost Optimized) ---
  Surname       Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Darlow      Leeds      GKP    3.9     0.008297                1205.253394
 Alderete Sunderland      DEF    4.0     0.045221                1183.081448
   Estève    Burnley      DEF    3.9     0.039990                1147.787330
Marc Guiu    Chelsea      FWD    4.2     0.017528                1163.850679

-------------------------------------------
Total Squad Cost:          £96.5m
Projected Starting Score:    1.01
Money in the Bank:         £3.5m
-------------------------------------------

```

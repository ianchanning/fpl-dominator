# FPL Dominator Squad Prophecy for GW17

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw17/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
    Surname           Team Position  Price  Final_Score
       Pope      Newcastle      GKP    5.1     0.079241
      Guéhi Crystal Palace      DEF    4.6     0.134271
  Calafiori        Arsenal      DEF    5.7     0.109682
   Chalobah        Chelsea      DEF    5.3     0.084109
B.Fernandes        Man Utd      MID    9.1     0.095803
    Semenyo    Bournemouth      MID    7.4     0.094841
     Rogers    Aston Villa      MID    7.3     0.089950
      Foden       Man City      MID    8.2     0.089882
    Caicedo        Chelsea      MID    5.7     0.088931
    Haaland       Man City      FWD   14.1     0.168441
    Ekitiké      Liverpool      FWD    9.0     0.083779

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname    Team Position  Price  Final_Score
   Darlow   Leeds      GKP    3.9     0.008123
   Estève Burnley      DEF    3.9     0.036999
  Hartman Burnley      DEF    4.0     0.043584
Marc Guiu Chelsea      FWD    4.2     0.010291

-------------------------------------------
Total Squad Cost:          £97.5m
Projected Starting Score:    1.12
Money in the Bank:         £2.5m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 154 players.
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
       Pope      Newcastle      GKP    5.1     0.079241                1179.941176
      Guéhi Crystal Palace      DEF    4.6     0.134271                1177.470588
  Calafiori        Arsenal      DEF    5.7     0.109682                1193.452489
     Virgil      Liverpool      DEF    5.9     0.061364                1134.217195
B.Fernandes        Man Utd      MID    9.1     0.095803                1135.660633
      Foden       Man City      MID    8.2     0.089882                1143.723982
     Wilson         Fulham      MID    5.8     0.086191                1126.570136
M.Fernandes       West Ham      MID    5.5     0.083954                1093.452489
    Haaland       Man City      FWD   14.1     0.168441                1143.723982
    Ekitiké      Liverpool      FWD    9.0     0.083779                1102.900452
     Thiago      Brentford      FWD    6.5     0.080509                1140.244344

--- BENCH (Potency & Cost Optimized) ---
 Surname       Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Darlow      Leeds      GKP    3.9     0.008123                1231.140271
Alderete Sunderland      DEF    4.0     0.060733                1187.153846
  Estève    Burnley      DEF    3.9     0.036999                1154.095023
  Ampadu      Leeds      MID    4.9     0.073163                1161.787330

-------------------------------------------
Total Squad Cost:          £96.2m
Projected Starting Score:    1.07
Money in the Bank:         £3.8m
-------------------------------------------

```

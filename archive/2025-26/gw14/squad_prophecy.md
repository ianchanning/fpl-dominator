# FPL Dominator Squad Prophecy for GW14

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw14/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score
    Raya        Arsenal      GKP    5.9     0.063320
   Guehi Crystal Palace      DEF    5.1     0.118305
   Muñoz Crystal Palace      DEF    6.1     0.083426
  Romero          Spurs      DEF    5.0     0.073335
   Foden       Man City      MID    8.4     0.099603
    Rice        Arsenal      MID    7.1     0.082042
E Le Fee     Sunderland      MID    4.9     0.077529
  Merino        Arsenal      MID    6.0     0.075913
 Semenyo    Bournemouth      MID    7.7     0.075306
 Haaland       Man City      FWD   15.0     0.132317
  Thiago      Brentford      FWD    6.8     0.082217

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname    Team Position  Price  Final_Score
     Darlow   Leeds      GKP    4.0     0.008164
     Estève Burnley      DEF    3.9     0.036388
Gudmundsson   Leeds      DEF    3.9     0.046410
  Marc Guiu Chelsea      FWD    4.2     0.010775

-------------------------------------------
Total Squad Cost:          £94.0m
Projected Starting Score:    0.96
Money in the Bank:         £6.0m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 192 players.
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
    Leno         Fulham      GKP    4.9     0.035141                1158.176471
   Guehi Crystal Palace      DEF    5.1     0.118305                1192.678733
   Muñoz Crystal Palace      DEF    6.1     0.083426                1192.678733
O'Reilly       Man City      DEF    5.2     0.050900                1155.208145
   Foden       Man City      MID    8.4     0.099603                1129.488688
    Rice        Arsenal      MID    7.1     0.082042                1142.095023
  Merino        Arsenal      MID    6.0     0.075913                1142.095023
 Semenyo    Bournemouth      MID    7.7     0.075306                1142.009050
Bruno G.      Newcastle      MID    6.8     0.072431                1086.556561
 Haaland       Man City      FWD   15.0     0.132317                1129.488688
  Thiago      Brentford      FWD    6.8     0.082217                1128.723982

--- BENCH (Potency & Cost Optimized) ---
    Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Dúbravka Burnley      GKP    4.0     0.035709                1178.972851
Gudmundsson   Leeds      DEF    3.9     0.046410                1224.954751
     Estève Burnley      DEF    3.9     0.036388                1178.972851
  Marc Guiu Chelsea      FWD    4.2     0.010775                1178.606335

-------------------------------------------
Total Squad Cost:          £95.1m
Projected Starting Score:    0.91
Money in the Bank:         £4.9m
-------------------------------------------

```

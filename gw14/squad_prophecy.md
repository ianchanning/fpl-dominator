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
    Raya        Arsenal      GKP    5.9     0.061331
   Guehi Crystal Palace      DEF    5.1     0.104481
   Muñoz Crystal Palace      DEF    6.1     0.080984
 Lacroix Crystal Palace      DEF    5.1     0.070074
   Foden       Man City      MID    8.4     0.088230
    Rice        Arsenal      MID    7.1     0.080301
 Semenyo    Bournemouth      MID    7.7     0.074793
Bruno G.      Newcastle      MID    6.8     0.069218
E Le Fee     Sunderland      MID    4.9     0.069026
 Haaland       Man City      FWD   15.0     0.129685
  Thiago      Brentford      FWD    6.8     0.080090

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname    Team Position  Price  Final_Score
     Darlow   Leeds      GKP    4.0     0.008166
     Estève Burnley      DEF    3.9     0.035416
Gudmundsson   Leeds      DEF    3.9     0.041034
  Marc Guiu Chelsea      FWD    4.2     0.010634

-------------------------------------------
Total Squad Cost:          £94.9m
Projected Starting Score:    0.91
Money in the Bank:         £5.1m
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
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1175).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
 Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
    Raya        Arsenal      GKP    5.9     0.061331                1165.800000
   Guehi Crystal Palace      DEF    5.1     0.104481                1191.600000
   Muñoz Crystal Palace      DEF    6.1     0.080984                1191.600000
 Lacroix Crystal Palace      DEF    5.1     0.070074                1191.600000
   Foden       Man City      MID    8.4     0.088230                1127.733333
    Rice        Arsenal      MID    7.1     0.080301                1139.466667
 Semenyo    Bournemouth      MID    7.7     0.074793                1136.466667
Bruno G.      Newcastle      MID    6.8     0.069218                1105.200000
E Le Fee     Sunderland      MID    4.9     0.069026                1173.466667
 Haaland       Man City      FWD   15.0     0.129685                1127.733333
  Thiago      Brentford      FWD    6.8     0.080090                1123.733333

--- BENCH (Potency & Cost Optimized) ---
    Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Dúbravka Burnley      GKP    4.0     0.035416                1171.800000
Gudmundsson   Leeds      DEF    3.9     0.041034                1224.600000
     Estève Burnley      DEF    3.9     0.035416                1171.800000
  Marc Guiu Chelsea      FWD    4.2     0.010634                1175.466667

-------------------------------------------
Total Squad Cost:          £94.9m
Projected Starting Score:    0.91
Money in the Bank:         £5.1m
-------------------------------------------

```

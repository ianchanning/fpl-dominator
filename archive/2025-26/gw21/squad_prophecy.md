# FPL Dominator Squad Prophecy for GW21

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw21/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
 Surname       Team Position  Price  Final_Score
   Roefs Sunderland      GKP    4.9     0.083022
 Gabriel    Arsenal      DEF    6.6     0.160688
Alderete Sunderland      DEF    4.1     0.110331
 O'Brien    Everton      DEF    4.9     0.096533
    Rice    Arsenal      MID    6.9     0.187364
   Stach      Leeds      MID    4.9     0.132103
  Schade  Brentford      MID    7.1     0.124086
Bruno G.  Newcastle      MID    6.8     0.124077
Casemiro    Man Utd      MID    5.5     0.121045
 Haaland   Man City      FWD   14.1     0.168715
  Thiago  Brentford      FWD    6.5     0.122651

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname          Team Position  Price  Final_Score
       John Nott'm Forest      GKP    4.0     0.009716
Gudmundsson         Leeds      DEF    3.8     0.044559
      Rodon         Leeds      DEF    3.9     0.085896
  Marc Guiu       Chelsea      FWD    4.2     0.010726

-------------------------------------------
Total Squad Cost:          £88.2m
Projected Starting Score:    1.43
Money in the Bank:         £11.8m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 161 players.
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
 Surname       Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Roefs Sunderland      GKP    4.9     0.083022                1186.428571
 Gabriel    Arsenal      DEF    6.6     0.160688                1184.904762
Alderete Sunderland      DEF    4.1     0.110331                1186.428571
 O'Brien    Everton      DEF    4.9     0.096533                1179.904762
    Rice    Arsenal      MID    6.9     0.187364                1128.285714
   Stach      Leeds      MID    4.9     0.132103                1149.857143
  Schade  Brentford      MID    7.1     0.124086                1184.666667
Bruno G.  Newcastle      MID    6.8     0.124077                1117.857143
Casemiro    Man Utd      MID    5.5     0.121045                1221.857143
 Haaland   Man City      FWD   14.1     0.168715                1149.571429
  Thiago  Brentford      FWD    6.5     0.122651                1184.666667

--- BENCH (Potency & Cost Optimized) ---
    Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Dúbravka Burnley      GKP    4.0     0.053107                1239.000000
      Rodon   Leeds      DEF    3.9     0.085896                1147.904762
Gudmundsson   Leeds      DEF    3.8     0.044559                1147.904762
  Marc Guiu Chelsea      FWD    4.2     0.010726                1118.809524

-------------------------------------------
Total Squad Cost:          £88.2m
Projected Starting Score:    1.43
Money in the Bank:         £11.8m
-------------------------------------------

```

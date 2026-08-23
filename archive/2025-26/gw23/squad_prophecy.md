# FPL Dominator Squad Prophecy for GW23

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw23/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
   Surname      Team Position  Price  Final_Score
  Pickford   Everton      GKP    5.6     0.094288
     Keane   Everton      DEF    4.7     0.137269
   Collins Brentford      DEF    5.0     0.128560
   Gabriel   Arsenal      DEF    6.6     0.107681
   Semenyo  Man City      MID    7.4     0.188322
  Aaronson     Leeds      MID    5.4     0.125839
     Wirtz Liverpool      MID    8.3     0.120862
   Caicedo   Chelsea      MID    5.7     0.120689
 Reijnders  Man City      MID    5.2     0.120066
   Haaland  Man City      FWD   14.1     0.162715
João Pedro   Chelsea      FWD    7.2     0.110226

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname        Team Position  Price  Final_Score
     Darlow       Leeds      GKP    3.9     0.019794
Gudmundsson       Leeds      DEF    3.8     0.050282
      Konsa Aston Villa      DEF    4.4     0.063420
  Marc Guiu     Chelsea      FWD    4.2     0.011209

-------------------------------------------
Total Squad Cost:          £91.5m
Projected Starting Score:    1.42
Money in the Bank:         £8.5m
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
   Surname      Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
  Pickford   Everton      GKP    5.6     0.094288                1188.904762
     Keane   Everton      DEF    4.7     0.137269                1188.904762
   Collins Brentford      DEF    5.0     0.128560                1203.333333
   Gabriel   Arsenal      DEF    6.6     0.107681                1182.190476
   Semenyo  Man City      MID    7.4     0.188322                1173.523810
  Aaronson     Leeds      MID    5.4     0.125839                1239.285714
     Wirtz Liverpool      MID    8.3     0.120862                1179.857143
   Caicedo   Chelsea      MID    5.7     0.120689                1070.523810
 Reijnders  Man City      MID    5.2     0.120066                1173.523810
   Haaland  Man City      FWD   14.1     0.162715                1173.523810
João Pedro   Chelsea      FWD    7.2     0.110226                1070.523810

--- BENCH (Potency & Cost Optimized) ---
    Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Dúbravka Burnley      GKP    4.0     0.067540                1184.476190
    Struijk   Leeds      DEF    4.3     0.065001                1192.285714
Gudmundsson   Leeds      DEF    3.8     0.050282                1192.285714
  Marc Guiu Chelsea      FWD    4.2     0.011209                1070.523810

-------------------------------------------
Total Squad Cost:          £91.5m
Projected Starting Score:    1.42
Money in the Bank:         £8.5m
-------------------------------------------

```

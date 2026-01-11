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
  Surname        Team Position  Price  Final_Score
    Roefs  Sunderland      GKP    4.9     0.088964
  Gabriel     Arsenal      DEF    6.6     0.160747
   Romero       Spurs      DEF    5.0     0.106530
 J.Timber     Arsenal      DEF    6.3     0.101987
     Rice     Arsenal      MID    6.9     0.187611
Tavernier Bournemouth      MID    5.5     0.130661
    Stach       Leeds      MID    4.9     0.130096
   Schade   Brentford      MID    7.1     0.123974
 Bruno G.   Newcastle      MID    6.8     0.122188
  Haaland    Man City      FWD   14.1     0.169408
   Thiago   Brentford      FWD    6.5     0.126673

--- BENCH (RUTHLESSLY Cost-Optimized) ---
    Surname          Team Position  Price  Final_Score
       John Nott'm Forest      GKP    4.0     0.011498
Gudmundsson         Leeds      DEF    3.8     0.072716
      Rodon         Leeds      DEF    3.9     0.051390
  Marc Guiu       Chelsea      FWD    4.2     0.010777

-------------------------------------------
Total Squad Cost:          £90.5m
Projected Starting Score:    1.45
Money in the Bank:         £9.5m
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
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1190).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
  Surname        Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
    Roefs  Sunderland      GKP    4.9     0.088964                1185.866667
  Gabriel     Arsenal      DEF    6.6     0.160747                1184.466667
   Romero       Spurs      DEF    5.0     0.106530                1164.933333
 J.Timber     Arsenal      DEF    6.3     0.101987                1184.466667
     Rice     Arsenal      MID    6.9     0.187611                1126.800000
Tavernier Bournemouth      MID    5.5     0.130661                1143.800000
    Stach       Leeds      MID    4.9     0.130096                1167.600000
   Schade   Brentford      MID    7.1     0.123974                1185.733333
 Bruno G.   Newcastle      MID    6.8     0.122188                1135.133333
  Haaland    Man City      FWD   14.1     0.169408                1144.866667
   Thiago   Brentford      FWD    6.5     0.126673                1185.733333

--- BENCH (Potency & Cost Optimized) ---
    Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
   Dúbravka Burnley      GKP    4.0     0.061250                1222.866667
Gudmundsson   Leeds      DEF    3.8     0.072716                1155.866667
      Rodon   Leeds      DEF    3.9     0.051390                1155.866667
  Marc Guiu Chelsea      FWD    4.2     0.010777                1113.466667

-------------------------------------------
Total Squad Cost:          £90.5m
Projected Starting Score:    1.45
Money in the Bank:         £9.5m
-------------------------------------------

```

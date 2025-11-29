# FPL Dominator Squad Prophecy for GW12

## PuLP Solver Output (Final Form v5)

```text
--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---
[+] Master configuration for PuLP solver loaded.
[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...
[+] SPP enrichment complete. Realities have been aligned.
[+] Final Form database (v5) forged at 'gw12/fpl_master_database_FINAL_v5.csv'.

>>> LAUNCHING FINAL FORM SIMULATION (V5)...

==================== FINAL FORM SQUAD (V5) FORGED ====================

--- STARTING XI (Final Score Maximized) ---
      Surname           Team Position  Price  Final_Score
    Henderson Crystal Palace      GKP    5.0         0.05
        Guéhi Crystal Palace      DEF    5.1         0.09
        Muñoz Crystal Palace      DEF    5.9         0.07
        Keane        Everton      DEF    4.5         0.07
      Semenyo    Bournemouth      MID    7.9         0.07
         Rice        Arsenal      MID    6.9         0.07
     Trossard        Arsenal      MID    6.9         0.06
Dewsbury-Hall        Everton      MID    4.9         0.06
  Gibbs-White  Nott'm Forest      MID    7.3         0.06
      Haaland       Man City      FWD   14.9         0.11
       Thiago      Brentford      FWD    6.5         0.07

--- BENCH (RUTHLESSLY Cost-Optimized) ---
  Surname    Team Position  Price  Final_Score
  Setford Arsenal      GKP    4.0         0.00
   Estève Burnley      DEF    3.9         0.03
  Hartman Burnley      DEF    4.0         0.05
Marc Guiu Chelsea      FWD    4.2         0.01

-------------------------------------------
Total Squad Cost:          £91.9m
Projected Starting Score:    0.78
Money in the Bank:         £8.1m
-------------------------------------------

```

## Pyomo Solver Output (Apotheosis v2)

```text
--- CHIMERA PYOMO ENGINE (V3 - TRINITY) ONLINE ---
[+] Master configuration for Pyomo solver loaded.
[+] Intelligence loaded. Analyzing 197 players.
[+] Pyomo ConcreteModel initialized.
[+] Sets (players) and Parameters (scores, prices, fdr, etc.) defined.
[+] Dual-layer decision variables created.
[+] Prime Directive (Final Apotheosis Objective) set.
[+] Applying the Chains of Reality (Game Constraints)...
[+] STRATEGIC CONSTRAINT: Red Zone limit active (Max 3 starters with FDR > 1250).
[+] All constraints are locked in.

>>> Summoning the GLPK Solver Demon...
>>> SOLVER TERMINATED. Status: optimal

==================== PYOMO SQUAD FORGED (V3 - TRINITY) ====================

--- STARTING XI (Final Score Maximized) ---
      Surname           Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
        Roefs     Sunderland      GKP    4.7         0.05                1260.266667
        Guéhi Crystal Palace      DEF    5.1         0.09                1175.800000
        Muñoz Crystal Palace      DEF    5.9         0.07                1175.800000
        Keane        Everton      DEF    4.5         0.07                1180.066667
      Semenyo    Bournemouth      MID    7.9         0.07                1143.133333
         Rice        Arsenal      MID    6.9         0.07                1154.533333
   J.Palhinha          Spurs      MID    5.5         0.06                1140.400000
      M.Salah      Liverpool      MID   14.2         0.06                1100.533333
Dewsbury-Hall        Everton      MID    4.9         0.06                1192.266667
      Haaland       Man City      FWD   14.9         0.11                1128.733333
       Thiago      Brentford      FWD    6.5         0.07                1159.266667

--- BENCH (Potency & Cost Optimized) ---
  Surname    Team Position  Price  Final_Score  Effective_FDR_Horizon_5GW
 Dúbravka Burnley      GKP    4.0         0.03                1193.533333
  Hartman Burnley      DEF    4.0         0.05                1193.533333
   Estève Burnley      DEF    3.9         0.03                1193.533333
Marc Guiu Chelsea      FWD    4.2         0.01                1211.733333

-------------------------------------------
Total Squad Cost:          £97.1m
Projected Starting Score:    0.78
Money in the Bank:         £2.9m
-------------------------------------------

```

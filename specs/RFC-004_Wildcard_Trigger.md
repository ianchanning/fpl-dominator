# RFC-004: Wildcard Trigger Protocol

## 1. Objective
Establish a mathematical trigger for the "Wildcard" (total squad reset) to avoid the "Sunk Cost Fallacy" and prevent the squad from getting trapped in a local minimum.

## 2. The "Divergence Delta"
The Wildcard should be triggered when the cost of migrating the current squad to the "North Star" (the ideal optimized squad) exceeds the value of the Wildcard itself.

### 2.1 Defining the Delta
$$\text{Divergence Delta} = \text{Points}(\text{North Star}) - \text{Points}(\text{Current Squad})$$

### 2.2 The Trigger Condition
The reset is triggered if:
1. The $\text{Divergence Delta}$ over the next $H$ weeks is greater than the projected point loss of taking multiple hits to get there.
2. The $\text{Divergence Delta}$ exceeds a "Critical Threshold" defined by the user's risk appetite.

## 3. Timing Constraints
- **Window:** Now until GW19.
- **Volatility Factor:** The trigger should be more sensitive during periods of high volatility (e.g., managerial changes at top clubs, international breaks, or injury crises).

## 4. Wildcard Evaluation Workflow
1. Generate the "North Star" squad for the next 5 GWs.
2. Calculate the "Migration Cost" (hits required to reach North Star).
3. Compare:
   - Path A: Manual migration via hits.
   - Path B: Immediate Wildcard reset.
   - Path C: Hold Wildcard for future volatility.
4. Recommend the path with the highest expected point return.

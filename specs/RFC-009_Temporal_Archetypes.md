# RFC-009: Temporal Archetypes (Decay Strategy Analysis)

## 1. Abstract
The current `fixture_weights` implementation uses a static decay array. This assumes a uniform "future-discounting" strategy. RFC-009 proposes the introduction of **Temporal Archetypes**—pre-defined weight profiles that represent different philosophies of FPL management. By running the Scenario Forge across these archetypes, we can distinguish between "Flash-in-the-pan" players and "Seasonal Cornerstones."

## 2. Proposed Archetypes

### 2.1 The Sniper (Hyper-Short Term)
- **Weight Profile:** `[1.0, 0.2, 0.05, 0.0, 0.0]`
- **Philosophy:** "The future is a lie." Focuses almost entirely on the immediate next fixture. Used to identify players with an imminent "폭발" (explosion) of points.

### 2.2 The Strategist (Long-Term Stability)
- **Weight Profile:** `[1.0, 0.9, 0.8, 0.7, 0.6]`
- **Philosophy:** "Consistency is King." Values the next 5 games almost equally. Used to build a squad that minimizes the need for transfers.

### 2.3 The Balanced (Current Baseline)
- **Weight Profile:** `[1.0, 0.5, 0.3, 0.2, 0.1]`
- **Philosophy:** Moderate decay. The middle ground.

## 3. Operational Integration
The `bamf forge` command will be expanded to allow the user to specify `archetypes` as a dimension of the matrix:
`bamf forge --archetypes sniper,strategist,balanced`

## 4. Analysis Output
The Forge will output a "Temporal Shift" report:
- **Core Assets:** Selected by all three archetypes (The "Must-Haves").
- **Short-Term Punts:** Selected only by the Sniper (The "Gamble").
- **Long-Term Holds:** Selected only by the Strategist (The "Patient Play").

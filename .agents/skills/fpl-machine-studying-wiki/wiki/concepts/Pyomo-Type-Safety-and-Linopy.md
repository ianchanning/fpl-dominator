# Pyomo Type Safety, Dynamic Metaprogramming & The Linopy Horizon

## 1. The Sovereign Law
Wrap Pyomo's dynamic metaprogramming components behind explicit `typing.Protocol` interfaces to maintain strict static analysis (`mypy`, `pyright`), paving the architectural path toward vectorized, data-centric `linopy` optimization pipelines.

---

## 2. The Trigger & Context
Pyomo is an industrial-strength algebraic modeling language, but its internal architecture relies heavily on dynamic attribute mutation:
- **The "Magic Attribute" Trap:** Declaring `model.x = Var()` attaches variables dynamically at runtime. Static type checkers see `ConcreteModel` as lacking attribute `x`, raising hundreds of false positive type errors.
- **The Container Indexing Obscurity:** Accessing indexed components `model.squad[player_id]` behaves like a dictionary at runtime, but static analyzers cannot infer the element type without stub files.
- **The Solution:** As specified in `BAMF-RFC-002_TYPE_SAFETY.md`, wrap raw Pyomo instances in a typed **Facade Pattern** function, isolating dynamic assignments to a single builder module while exposing typed data structures to the rest of the application.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Raw Pyomo Metaprogramming | Typed Facade / Linopy Architecture |
| :--- | :--- | :--- |
| **Static Verification** | Opaque to `mypy`/`pyright`; requires numerous `# type: ignore` comments. | **100% Type-Safe:** All decision variables and solver parameters adhere to explicit `Protocol` definitions. |
| **Constraint Construction** | Explicit imperative Python `for` loops. | **Vectorized & Declarative:** Constraint matrices defined directly over `pandas` DataFrames / `xarray`. |
| **Refactoring Safety** | Renaming a model variable at runtime causes silent `AttributeError` during solve. | Compile-time / lint-time attribute validation. |

---

## 4. The Implementation Pattern

### 1. The Typed Solver Protocol (`protocols/types.py`)

```python
from typing import Protocol, Dict, Any, List
import pandas as pd


class OptimizationResult(Protocol):
    squad_ids: List[str]
    starter_ids: List[str]
    captain_id: str
    vice_captain_id: str
    expected_points: float
    total_cost: float


class ChimeraSolverProtocol(Protocol):
    def solve(self, data: pd.DataFrame, budget: float) -> OptimizationResult: ...
```

### 2. The Long-Term Linopy Vectorized Migration

```python
import linopy
import xarray as xr


def solve_with_linopy(df: pd.DataFrame, budget: float = 100.0) -> xr.Dataset:
    m = linopy.Model()

    # 1. Vectorized Binary Variables
    squad = m.add_variables(binary=True, coords=[df.index], name="squad")
    starter = m.add_variables(binary=True, coords=[df.index], name="starter")

    # 2. Vectorized Linear Constraints
    m.add_constraints(squad.sum() == 15, name="squad_size")
    m.add_constraints(starter.sum() == 11, name="starter_size")
    m.add_constraints((df["Price"] * squad).sum() <= budget, name="budget_cap")
    m.add_constraints(starter <= squad, name="starter_in_squad")

    # 3. Vectorized Objective
    m.add_objective((df["Expected_Points"] * starter).sum(), sense="max")

    m.solve(solver_name="glpk")
    return m.solution
```

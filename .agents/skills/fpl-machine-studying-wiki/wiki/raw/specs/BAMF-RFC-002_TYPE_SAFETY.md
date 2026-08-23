# BAMF-RFC-002: THE STRONGLY TYPED CHIMERA (v1.0)

**Status:** PROPOSED (Future Voyage) `(⇌)`
**Objective:** Eliminate dynamic attribute purgatory and achieve 100% type safety in optimization models.
**Core Philosophy:** Code is Law. Types are the Constitution. **EX DATA, VERITAS.**

---

## I. THE PROBLEM: PYOMO'S DYNAMIC CHAOS

Pyomo is a powerful modeling language, but it was forged in an era before Python type hints reigned supreme. Its design relies heavily on **metaprogramming** and **dynamic attribute assignment**, which are anathema to static analysis tools like `pyright` and `mypy`.

### 1.1 The "Magic Attribute" Trap
When you declare a Pyomo component:
```python
model = ConcreteModel()
model.x = Var()  # Dynamic assignment
```
To a type checker, `model` is just a generic `ConcreteModel` class. It has no idea that `.x` exists. This leads to the "Cannot access attribute" errors we see in `chimera_pyomo_v2.py`.

### 1.2 The Indexing Nightmare
Pyomo's `IndexedBlock` and `IndexedVar` components behave like dictionaries at runtime but are often typed as generic container classes. Accessing `model.x[i]` is valid Python but opaque to static analysis without extensive stub files (`.pyi`) which do not officially exist for Pyomo.

---

## II. STRATEGY A: THE "WRAPPED" CHIMERA (Near-Term)

If we stick with Pyomo, we must wrap the dynamic chaos in a strongly typed shell. This uses the **Facade Pattern**.

### 2.1 The Typed Protocol
Instead of passing the raw `ConcreteModel` around, we define a `Protocol` or `Dataclass` that strictly defines the interface our solver expects.

```python
from typing import Protocol, Dict

class ChimeraModel(Protocol):
    # Explicitly declare the components we expect to exist
    squad_vars: Dict[str, Any]
    starter_vars: Dict[str, Any]
    objective_value: float

    def solve(self) -> str: ...
```

### 2.2 The "Builder" Function
Isolate the Pyomo chaos inside a single function that returns this Typed object. The rest of the codebase (the "Functional Core") never touches the raw Pyomo model, only the typed interface.

---

## III. STRATEGY B: THE "LINOPY" MIGRATION (Long-Term)

To truly embrace functional programming and category theory, we should migrate to a library designed with modern data structures in mind.

### 3.1 Why Linopy?
*   **Data-Centric:** Built on `xarray` and `pandas`. Variables are not isolated scalar objects but N-dimensional labeled arrays.
*   **Vectorized:** Constraints are defined using vectorized operations (e.g., `x.sum() <= 100`), which is naturally cleaner and faster than Pyomo's explicit loops.
*   **Typed:** Linopy supports type hints and integrates with static analysis tools out of the box.

### 3.2 The Functional Dream
With `linopy`, the optimization model becomes a transformation pipeline:
`Data (Pandas) -> Variables (Xarray) -> Constraints (Vectorized) -> Solution (Xarray)`

This aligns perfectly with a functional architecture where the solver is just a pure function:
`solve :: GameState -> Constraints -> OptimizationResult`

---

## IV. RECOMMENDATION

1.  **Phase 1 (Now):** Accept the Pyomo warnings or suppress them with specific `# type: ignore` directives. The cost of refactoring Pyomo now is too high for the benefit.
2.  **Phase 2 (Future):** Pilot a **Linopy** implementation for a small, isolated module (e.g., `chimera_scenarios.py`). If the DX (Developer Experience) proves superior, plan a full migration.

**EX DATA, VERITAS. `(⇌)`**

# ORBITAL

**ORBITAL** is a modular gravitational simulation engine focused on numerical accuracy, physical validation, and scalable N-body computation.

The project was built as a computational laboratory for experimenting with gravitational systems, numerical integration, physical invariants, and performance optimization using Python and NumPy.

> The goal is not only to simulate motion, but to verify whether the simulation behaves according to the underlying physics.

---

## Overview

ORBITAL models systems of gravitationally interacting bodies and numerically integrates their motion over time.

The engine currently supports:

* Two-body and N-body gravitational systems
* Newtonian gravitational acceleration
* Vectorized and blocked N-body computation
* Velocity Verlet integration
* Total energy calculation
* Angular momentum calculation
* Center of mass calculation
* Physical and numerical validation
* Automated test coverage
* Performance benchmarking

The current implementation focuses on **2D systems**, while the architecture is designed to keep the physics and simulation layers modular.

---

## Why ORBITAL?

A gravitational simulator can produce visually convincing trajectories while still being numerically incorrect.

ORBITAL therefore treats **physical validation as a first-class concern**.

Instead of only asking:

> "Does the orbit look correct?"

the project also asks:

* Is energy conserved?
* Is angular momentum conserved?
* Is the center of mass behaving correctly?
* Does the numerical solution converge as the timestep decreases?
* Is the integrator reversible?
* Does the N-body implementation agree with the reference implementation?
* How does computational cost scale with the number of bodies?

This makes ORBITAL closer to a small **computational physics laboratory** than a simple orbital animation.

---

## Architecture

The project is organized into separate physics and simulation layers.

```text
orbital/
│
├── physics/
│   ├── body.py
│   ├── gravity.py
│   ├── gravity_solver.py
│   ├── gravity_solver_protocol.py
│   ├── energy.py
│   ├── total_energy.py
│   ├── angular_momentum.py
│   ├── center_of_mass.py
│   ├── orbit.py
│   ├── velocity_verlet.py
│   └── integrator_protocol.py
│
└── simulation/
    ├── engine.py
    └── state.py

tests/
benchmarks/
examples/
```

### Physics layer

Responsible for physical laws and numerical algorithms.

It contains:

* body representation
* gravitational acceleration
* energy
* angular momentum
* center of mass
* orbital calculations
* numerical integration
* solver protocols

### Simulation layer

Responsible for coordinating the simulation.

The `SimulationEngine` connects:

```text
Bodies
   ↓
Gravity Solver
   ↓
Acceleration
   ↓
Integrator
   ↓
New State
```

This separation allows the numerical solver and integrator to evolve independently.

---

## Gravitational Model

The engine uses Newton's law of universal gravitation.

For two bodies:

$$
F = G\frac{m_1m_2}{r^2}
$$

where:

* $F$ is the gravitational force
* $G$ is the gravitational constant
* $m_1$ and $m_2$ are the masses
* $r$ is the distance between the bodies

The acceleration of body $i$ caused by body $j$ is:

$$
\vec{a}_{ij}
=
Gm_j
\frac{\vec{r}_j-\vec{r}_i}
{|\vec{r}_j-\vec{r}_i|^3}
$$

For an N-body system, the total acceleration is the sum of the contributions from all other bodies:

$$
\vec{a}_i
=
G
\sum_{j\neq i}
m_j
\frac{\vec{r}_j-\vec{r}_i}
{|\vec{r}_j-\vec{r}_i|^3}
$$

This produces an $O(N^2)$ algorithm because every body can interact with every other body.

---

## Numerical Integration

ORBITAL uses the **Velocity Verlet** integration method.

Velocity Verlet is particularly suitable for gravitational simulations because it is a symplectic integration method that provides good long-term energy behavior.

The position update is:

$$
\vec{x}_{t+\Delta t}
=
\vec{x}_t
+
\vec{v}_t\Delta t
+
\frac{1}{2}\vec{a}_t\Delta t^2
$$

The new acceleration is then calculated, followed by the velocity update:

$$
\vec{v}_{t+\Delta t}
=
\vec{v}_t
+
\frac{1}{2}
\left(
\vec{a}_t+\vec{a}_{t+\Delta t}
\right)
\Delta t
$$

The implementation separates the integration contract from the concrete `VelocityVerlet` implementation through a protocol.

This makes it possible to introduce alternative integrators in the future without coupling them directly to the simulation engine.
---

## Numerical Validation

ORBITAL does not rely only on visual inspection.

The project contains automated tests for mathematical properties and physical invariants.

### Energy conservation

For a stable two-body orbit using a timestep of 21,600 seconds:

```text
Maximum relative energy error ≈ 2.10 × 10⁻⁸
```

The simulation therefore maintains excellent energy conservation under the tested configuration.

### Angular momentum

The maximum relative angular momentum error measured in the validation suite is approximately:

```text
8.54 × 10⁻¹⁵
```

### Time reversibility

The Velocity Verlet implementation was also tested for temporal reversibility.

Measured errors:

```text
Position error  ≈ 5.3 × 10⁻¹⁴
Velocity error  ≈ 5.4 × 10⁻¹⁴
```

### Convergence

The numerical solution exhibits the expected second-order behavior.

Example closure errors:

| Configuration    | Closure Error |
| ---------------- | ------------: |
| 500 steps/orbit  |  3.307 × 10⁻⁴ |
| 1000 steps/orbit |  8.268 × 10⁻⁵ |
| 2000 steps/orbit |  2.067 × 10⁻⁵ |

Reducing the timestep by a factor of two reduces the error by approximately a factor of four, which is consistent with a second-order integration method.

---

## N-Body Validation

The N-body implementation is validated against a reference gravitational solver.

The test suite also verifies conservation properties for multi-body systems.

Measured errors include:

```text
Linear momentum error      ≈ 3.3 × 10⁻¹⁵
Angular momentum error     ≈ 1.25 × 10⁻¹⁵
```

These tests help ensure that vectorization and performance optimizations do not alter the physical behavior of the solver.

---

## Performance

The gravitational solver uses NumPy vectorization combined with **blocked computation**.

A naive vectorized implementation can require large intermediate matrices as the number of bodies increases.

Blocking processes subsets of bodies at a time:

```text
N bodies
   │
   ├── Block 1
   ├── Block 2
   ├── Block 3
   └── ...
        ↓
   Accelerations
```

This significantly reduces peak memory usage while maintaining vectorized computation.

### Example scalability benchmark

On the development machine:

| Bodies | Blocked Solver |
| -----: | -------------: |
| 10,000 |        ~9.24 s |
| 20,000 |        ~36.1 s |

The current gravitational calculation remains \(O(N^2)\), so computation grows rapidly as the number of bodies increases.

This is an intentional limitation of the current architecture and provides a clear direction for future optimization.

---

## Reference vs Vectorized Solver

The project also includes benchmark infrastructure comparing the original reference implementation with the optimized vectorized solver.

Example results:

|     N | Speedup |
| ----: | ------: |
|    10 |   5.79× |
|    50 | 105.67× |
|   100 |  47.31× |
|   250 |  50.77× |
|   500 |  58.06× |
| 1,000 |  59.40× |

The purpose of these benchmarks is not simply to demonstrate faster execution, but to verify that performance optimizations preserve the same physical result.

---

## Tests

The project currently contains a comprehensive automated test suite covering:

* body validation
* gravity calculations
* solver equivalence
* solver positions
* N-body physics
* total energy
* angular momentum
* center of mass
* orbital behavior
* Velocity Verlet
* integrator protocols
* simulation engine
* convergence
* physical invariants

Current status:

```text
85 passed
```

Run the complete test suite with:

```bash
pytest -q
```

---

## Running the Example

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -e ".[dev]"
```
**### Optional Visualization**

To install the visualization dependencies:

```bash
pip install -e ".[visualization]"

Run the two-body experiment:

```bash
python examples/two_body.py
```

The experiment configuration can be adjusted in:

```text
examples/two_body_config.py
```

This makes it possible to experiment with parameters such as:

* timestep
* simulation duration
* initial velocity
* masses
* orbital configuration
* energy sampling

---

## Project Structure

```text
.
├── benchmarks/
│   ├── benchmark_blocked_scalability.py
│   ├── benchmark_blocked_solver.py
│   └── benchmark_gravity_solver.py
│
├── examples/
│   ├── two_body.py
│   └── two_body_config.py
│
├── src/
│   └── orbital/
│       ├── physics/
│       └── simulation/
│
├── tests/
│
├── .gitignore
└── pyproject.toml
```

---

## Current Limitations

ORBITAL is intentionally focused on a well-defined scope.

Current limitations include:

* 2D simulations
* Newtonian gravity
* \(O(N^2)\) gravitational computation
* No GPU acceleration
* No parallel N-body solver
* No Barnes-Hut approximation
* No relativistic effects
* No collision detection system
* No graphical interface yet

These limitations are part of the project's development roadmap rather than hidden constraints.

---

## Roadmap

### V0.1 — Fundamentals

* [x] Body model
* [x] Newtonian gravity
* [x] Simulation state
* [x] Velocity Verlet
* [x] Energy calculation
* [x] Angular momentum
* [x] Center of mass
* [x] Automated tests

### V0.2 — N-Body

* [x] N-body gravitational solver
* [x] Vectorization
* [x] Blocked computation
* [x] Solver protocols
* [x] Scalability benchmarks

### V0.3 — Numerical Precision

* [x] Energy validation
* [x] Angular momentum validation
* [x] Time reversibility
* [x] Convergence testing
* [x] Reference solver comparison

### V0.4 — Visualization

* [ ] Orbital visualization
* [ ] Trajectory rendering
* [ ] Energy/error graphs
* [ ] Simulation playback

### V0.5 — Real Systems

* [ ] Solar-system presets
* [ ] Physical constants and units
* [ ] Configurable initial conditions
* [ ] Real astronomical scenarios

### V0.6 — Experiments

* [ ] Experiment runner
* [ ] Result export
* [ ] CSV output
* [ ] Reproducible experiment configurations

### V0.7 — Procedural Systems

* [ ] Random system generation
* [ ] Initial-condition generators
* [ ] Stability experiments

### V0.8 — Stability

* [ ] Collision detection
* [ ] Close-encounter detection
* [ ] Numerical instability detection
* [ ] Automatic warnings

### V0.9 — Data & Statistics

* [ ] Statistical analysis
* [ ] Long-term orbital studies
* [ ] Parameter sweeps
* [ ] Automated experiment comparison

### V1.0 — Computational Laboratory

* [ ] Unified experiment interface
* [ ] Complete visualization layer
* [ ] Reproducible experiments
* [ ] Exportable scientific results

### Post-V1.0

Possible future research directions include:

* Barnes-Hut gravitational approximation
* Parallel computation
* GPU acceleration
* Higher-dimensional simulations
* Machine learning experiments
* Real astronomical datasets

---

## Design Philosophy

ORBITAL follows a few principles:

**Correctness before complexity.**

A sophisticated optimization is not useful if it changes the physical result.

**Validation before visualization.**

A trajectory looking correct is not enough. Physical invariants and numerical properties must also be tested.

**Modularity before premature optimization.**

Physics, numerical integration, and simulation orchestration are kept separated so each component can evolve independently.

**Performance with evidence.**

Optimizations are benchmarked instead of being assumed to be faster.

**Local-first.**

The project is designed to run locally without external APIs, cloud services, or paid infrastructure.

---

## Technology

* **Python**
* **NumPy**
* **pytest**
* **Ruff**
* **Git / GitHub**

---

## License

This project is open source. See the repository license for details.

---

## Author

Developed by **Arthur Santos** as an independent computational physics and software engineering project.

The project combines numerical methods, physics, software architecture, testing, and performance engineering into a single experimental platform.

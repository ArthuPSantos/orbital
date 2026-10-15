# ORBITAL

**A computational laboratory for gravitational systems.**

ORBITAL is a desktop application for simulating and analyzing gravitational interactions between a star and a planet. Built with Python, it combines numerical physics, real-time visualization, and physical analysis in an interactive environment.

### Features

- **Simulation:** Explore gravitational motion using the Velocity Verlet integration method.
- **Visualization:** Observe orbital trajectories and the motion of celestial bodies.
- **Physical Analysis:** Track distance, velocity, total energy, and angular momentum over time.
- **Numerical Metrics:** Evaluate energy and angular momentum conservation.
- **User Guide:** Learn about the simulation parameters, units, and physical results.

### Installation

**Requirements:** Python 3.12 or later and Git.

1. Clone the repository:

   ```bash
   git clone https://github.com/ArthurPSantos/orbital.git
   cd orbital
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the project and development dependencies:

   ```bash
   python -m pip install -e ".[dev]"
   ```

### Run the Application

```bash
python app/main.py
```

### Run Tests

```bash
python -m pytest
```

---

*ORBITAL — Exploring gravitational dynamics through computational physics.*
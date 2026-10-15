import time

import numpy as np
from experiment_config import ExperimentConfig

from orbital.physics.angular_momentum import (
    total_angular_momentum,
)
from orbital.physics.body import Body
from orbital.physics.total_energy import total_energy
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState

SOLAR_RADIUS_M = 6.957e8
EARTH_RADIUS_M = 6.371e6


def precision_to_dt(precision: str) -> float:
    if precision == "FAST":
        return 86_400.0

    if precision == "BALANCED":
        return 21_600.0

    if precision == "HIGH":
        return 3_600.0

    if precision == "CUSTOM":
        return 21_600.0

    raise ValueError(
        f"Unsupported precision: {precision}"
    )


def create_manual_simulation(
    config: ExperimentConfig,
) -> SimulationEngine:
    star = Body(
        mass=config.star_mass_kg,
        position=np.array(
            [0.0, 0.0],
            dtype=float,
        ),
        velocity=np.array(
            [0.0, 0.0],
            dtype=float,
        ),
        radius=SOLAR_RADIUS_M,
    )

    planet = Body(
        mass=config.planet_mass_kg,
        position=np.array(
            [config.distance_m, 0.0],
            dtype=float,
        ),
        velocity=np.array(
            [0.0, config.velocity_m_per_s],
            dtype=float,
        ),
        radius=EARTH_RADIUS_M,
    )

    state = SimulationState(
        bodies=[
            star,
            planet,
        ]
    )

    dt = precision_to_dt(
        config.precision
    )

    return SimulationEngine(
        state=state,
        dt=dt,
    )


def relative_error(
    initial: float,
    final: float,
) -> float:
    denominator = abs(initial)

    if denominator == 0.0:
        return 0.0

    return abs(
        final - initial
    ) / denominator


def run_manual_experiment(
    config: ExperimentConfig,
) -> dict:
    engine = create_manual_simulation(
        config
    )

    initial_energy = total_energy(
        engine.state.bodies
    )

    initial_angular_momentum = (
        total_angular_momentum(
            engine.state.bodies
        )
    )

    dt = engine.dt
    total_time = config.duration_s

    steps = int(
        total_time / dt
    )

    trajectory_star = [
        engine.state.bodies[0].position.copy()
    ]

    trajectory_planet = [
        engine.state.bodies[1].position.copy()
    ]

    trajectory_velocity = [
        engine.state.bodies[1].velocity.copy()
    ]

    trajectory_times = [
        engine.state.time
    ]

    energy_history = [
        initial_energy
    ]

    angular_momentum_history = [
        initial_angular_momentum
    ]

    distance_history = [
        np.linalg.norm(
            engine.state.bodies[1].position
        )
    ]

    velocity_history = [
        np.linalg.norm(
            engine.state.bodies[1].velocity
        )
    ]

    start_time = time.perf_counter()

    for _ in range(steps):
        engine.step()

        planet = engine.state.bodies[1]

        trajectory_star.append(
            engine.state.bodies[0].position.copy()
        )

        trajectory_planet.append(
            planet.position.copy()
        )

        trajectory_velocity.append(
            planet.velocity.copy()
        )

        trajectory_times.append(
            engine.state.time
        )

        energy_history.append(
            total_energy(
                engine.state.bodies
            )
        )

        angular_momentum_history.append(
            total_angular_momentum(
                engine.state.bodies
            )
        )

        distance_history.append(
            np.linalg.norm(
                planet.position
            )
        )

        velocity_history.append(
            np.linalg.norm(
                planet.velocity
            )
        )

    computation_time = (
        time.perf_counter()
        - start_time
    )

    final_energy = total_energy(
        engine.state.bodies
    )

    final_angular_momentum = (
        total_angular_momentum(
            engine.state.bodies
        )
    )

    energy_error = relative_error(
        initial_energy,
        final_energy,
    )

    angular_momentum_error = relative_error(
        initial_angular_momentum,
        final_angular_momentum,
    )

    return {
        "engine": engine,
        "trajectory_star": np.array(
            trajectory_star
        ),
        "trajectory_planet": np.array(
            trajectory_planet
        ),
        "trajectory_velocity": np.array(
            trajectory_velocity
        ),
        "trajectory_times": np.array(
            trajectory_times
        ),
        "energy_history": np.array(
            energy_history
        ),
        "angular_momentum_history": np.array(
            angular_momentum_history
        ),
        "distance_history": np.array(
            distance_history
        ),
        "velocity_history": np.array(
            velocity_history
        ),
        "steps": steps,
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "energy_error": energy_error,
        "initial_angular_momentum": (
            initial_angular_momentum
        ),
        "final_angular_momentum": (
            final_angular_momentum
        ),
        "angular_momentum_error": (
            angular_momentum_error
        ),
        "computation_time": (
            computation_time
        ),
    }
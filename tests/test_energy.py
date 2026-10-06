import numpy as np

from orbital.physics.body import Body
from orbital.physics.energy import (
    gravitational_potential_energy,
    kinetic_energy,
)
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def test_kinetic_energy():
    """A energia cinética deve seguir K = 1/2 mv²."""

    body = Body(
        mass=2.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([3.0, 4.0]),
        radius=1.0,
    )

    assert kinetic_energy(body) == 25.0


def test_gravitational_potential_energy():
    """A energia potencial deve seguir U = -Gm1m2/r."""

    body_a = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=2.0,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    expected = (
        -GRAVITATIONAL_CONSTANT
        * 1.0
        * 2.0
        / 10.0
    )

    assert np.isclose(
        gravitational_potential_energy(body_a, body_b),
        expected,
    )



def test_two_body_energy_is_conserved():
    """A energia mecânica deve permanecer aproximadamente constante."""

    star_mass = 1.989e30
    planet_mass = 5.972e24

    orbital_radius = 1.496e11

    orbital_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT
        * star_mass
        / orbital_radius
    )

    star = Body(
        mass=star_mass,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=6.9634e8,
    )

    planet = Body(
        mass=planet_mass,
        position=np.array([orbital_radius, 0.0]),
        velocity=np.array([0.0, orbital_velocity]),
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[star, planet],
    )

    engine = SimulationEngine(
        state=state,
        dt=86400.0,
    )

    def total_energy() -> float:
        """Calcula a energia mecânica total do sistema."""

        kinetic = sum(
            kinetic_energy(body)
            for body in state.bodies
        )

        potential = gravitational_potential_energy(
            star,
            planet,
        )

        return kinetic + potential

    initial_energy = total_energy()

    maximum_relative_error = 0.0

    for _ in range(365):
        engine.step()

        current_energy = total_energy()

        relative_error = abs(
            (current_energy - initial_energy)
            / initial_energy
        )

        maximum_relative_error = max(
            maximum_relative_error,
            relative_error,
        )

    assert maximum_relative_error < 1e-3


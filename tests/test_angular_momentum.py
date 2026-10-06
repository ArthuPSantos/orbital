import numpy as np

from orbital.physics.angular_momentum import (
    angular_momentum,
    total_angular_momentum,
)
from orbital.physics.body import Body
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def test_angular_momentum():
    """O momento angular deve seguir L = m(xvy - yvx)."""

    body = Body(
        mass=2.0,
        position=np.array([3.0, 4.0]),
        velocity=np.array([5.0, 6.0]),
        radius=1.0,
    )

    expected = 2.0 * (3.0 * 6.0 - 4.0 * 5.0)

    assert angular_momentum(body) == expected


def test_total_angular_momentum_uses_center_of_mass():
    """O momento angular total deve ser calculado no referencial do CM."""

    body_a = Body(
        mass=2.0,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 3.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=2.0,
        position=np.array([14.0, 0.0]),
        velocity=np.array([0.0, 1.0]),
        radius=1.0,
    )

    result = total_angular_momentum(
        [body_a, body_b]
    )

    expected = -8.0

    assert np.isclose(result, expected)


def test_two_body_angular_momentum_is_conserved():
    """O momento angular total deve permanecer aproximadamente constante."""

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

    initial_momentum = total_angular_momentum(
        state.bodies
    )

    for _ in range(365):
        engine.step()

    final_momentum = total_angular_momentum(
        state.bodies
    )

    relative_error = abs(
        (final_momentum - initial_momentum)
        / initial_momentum
    )

    assert relative_error < 1e-10



def test_two_body_angular_momentum_is_conserved_over_many_orbits():
    """
    Verifica a conservação do momento angular em uma simulação
    de dois corpos durante várias órbitas.

    Para uma força gravitacional central, não existe torque externo
    sobre o sistema. Portanto, o momento angular total deve permanecer
    constante:

        L = constante

    O teste mede o maior erro relativo encontrado durante 20 órbitas.
    """

    star_mass = 1.989e30
    planet_mass = 5.972e24

    separation = 1.496e11

    total_mass = star_mass + planet_mass

    # Velocidade relativa para uma órbita circular.
    relative_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT
        * total_mass
        / separation
    )

    # Período orbital analítico.
    orbital_period = 2.0 * np.pi * np.sqrt(
        separation**3
        / (
            GRAVITATIONAL_CONSTANT
            * total_mass
        )
    )

    # 1000 passos por órbita.
    steps_per_orbit = 1000
    dt = orbital_period / steps_per_orbit

    star = Body(
        mass=star_mass,
        position=np.array([
            -planet_mass / total_mass * separation,
            0.0,
        ]),
        velocity=np.array([
            0.0,
            -planet_mass / total_mass * relative_velocity,
        ]),
        radius=6.9634e8,
    )

    planet = Body(
        mass=planet_mass,
        position=np.array([
            star_mass / total_mass * separation,
            0.0,
        ]),
        velocity=np.array([
            0.0,
            star_mass / total_mass * relative_velocity,
        ]),
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[star, planet],
    )

    engine = SimulationEngine(
        state=state,
        dt=dt,
    )

    initial_angular_momentum = total_angular_momentum(
        state.bodies
    )

    maximum_relative_error = 0.0

    # Simula 20 órbitas.
    for _ in range(20 * steps_per_orbit):
        engine.step()

        current_angular_momentum = total_angular_momentum(
            state.bodies
        )

        relative_error = abs(
            (
                current_angular_momentum
                - initial_angular_momentum
            )
            / initial_angular_momentum
        )

        maximum_relative_error = max(
            maximum_relative_error,
            relative_error,
        )

    print(
        f"Erro máximo relativo do momento angular: "
        f"{maximum_relative_error:.12e}"
    )

    # O momento angular deve permanecer praticamente constante.
    assert maximum_relative_error < 1e-10


import numpy as np
import pytest

from orbital.physics.body import Body
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.physics.velocity_verlet import VelocityVerlet
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def test_velocity_verlet_step():
    """O integrador deve calcular corretamente um passo."""

    integrator = VelocityVerlet()

    position = np.array([0.0, 0.0])
    velocity = np.array([1.0, 0.0])
    acceleration = np.array([0.0, 0.0])

    def acceleration_function(position):
        return np.array([0.0, 0.0])

    result = integrator.step(
        position=position,
        velocity=velocity,
        acceleration=acceleration,
        acceleration_function=acceleration_function,
        dt=1.0,
    )

    assert np.allclose(
        result.position,
        np.array([1.0, 0.0]),
    )

    assert np.allclose(
        result.velocity,
        np.array([1.0, 0.0]),
    )

    assert np.allclose(
        result.acceleration,
        np.array([0.0, 0.0]),
    )


def test_velocity_verlet_with_constant_acceleration():
    """O integrador deve reproduzir corretamente uma aceleração constante."""

    integrator = VelocityVerlet()

    position = np.array([0.0, 0.0])
    velocity = np.array([0.0, 0.0])
    acceleration = np.array([2.0, 0.0])

    def acceleration_function(position):
        return np.array([2.0, 0.0])

    result = integrator.step(
        position=position,
        velocity=velocity,
        acceleration=acceleration,
        acceleration_function=acceleration_function,
        dt=1.0,
    )

    assert np.allclose(
        result.position,
        np.array([1.0, 0.0]),
    )

    assert np.allclose(
        result.velocity,
        np.array([2.0, 0.0]),
    )

    assert np.allclose(
        result.acceleration,
        np.array([2.0, 0.0]),
    )


def test_velocity_verlet_calculates_initial_acceleration_when_missing():
    """O integrador deve calcular a aceleração quando ela não é fornecida."""

    integrator = VelocityVerlet()

    position = np.array([0.0, 0.0])
    velocity = np.array([1.0, 0.0])

    def acceleration_function(position):
        return np.array([2.0, 0.0])

    result = integrator.step(
        position=position,
        velocity=velocity,
        acceleration=None,
        acceleration_function=acceleration_function,
        dt=1.0,
    )

    assert np.allclose(
        result.position,
        np.array([2.0, 0.0]),
    )

    assert np.allclose(
        result.velocity,
        np.array([3.0, 0.0]),
    )


def test_velocity_verlet_rejects_invalid_dt():
    """O integrador deve rejeitar dt inválido."""

    integrator = VelocityVerlet()

    position = np.zeros(2)
    velocity = np.zeros(2)
    acceleration = np.zeros(2)

    def acceleration_function(position):
        return np.zeros(2)

    with pytest.raises(ValueError):
        integrator.step(
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            acceleration_function=acceleration_function,
            dt=0.0,
        )

    with pytest.raises(ValueError):
        integrator.step(
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            acceleration_function=acceleration_function,
            dt=-1.0,
        )


def test_velocity_verlet_is_reversible():
    """
    Verifica a reversibilidade temporal do Velocity Verlet.

    O experimento executa duas etapas:

    1. Avança o sistema durante vários passos.
    2. Inverte as velocidades e avança novamente.

    Ao final, as velocidades são invertidas novamente.

    Para um integrador reversível, o sistema deve retornar
    praticamente ao estado inicial.
    """

    star_mass = 1.989e30
    planet_mass = 5.972e24
    separation = 1.496e11

    total_mass = star_mass + planet_mass

    relative_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT
        * total_mass
        / separation
    )

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

    orbital_period = 2.0 * np.pi * np.sqrt(
        separation**3
        / (
            GRAVITATIONAL_CONSTANT
            * total_mass
        )
    )

    steps = 1000
    dt = orbital_period / steps

    engine = SimulationEngine(
        state=state,
        dt=dt,
    )

    initial_positions = [
        body.position.copy()
        for body in state.bodies
    ]

    initial_velocities = [
        body.velocity.copy()
        for body in state.bodies
    ]

    for _ in range(steps):
        engine.step()

    for body in state.bodies:
        body.velocity *= -1.0

    for _ in range(steps):
        engine.step()

    for body in state.bodies:
        body.velocity *= -1.0

    maximum_position_error = 0.0
    maximum_velocity_error = 0.0

    for body, initial_position, initial_velocity in zip(
        state.bodies,
        initial_positions,
        initial_velocities,
    ):
        position_error = np.linalg.norm(
            body.position - initial_position
        )

        velocity_error = np.linalg.norm(
            body.velocity - initial_velocity
        )

        maximum_position_error = max(
            maximum_position_error,
            position_error,
        )

        maximum_velocity_error = max(
            maximum_velocity_error,
            velocity_error,
        )

    relative_position_error = (
        maximum_position_error / separation
    )

    relative_velocity_error = (
        maximum_velocity_error / relative_velocity
    )

    print(
        f"Erro relativo máximo de posição: "
        f"{relative_position_error:.12e}"
    )

    print(
        f"Erro relativo máximo de velocidade: "
        f"{relative_velocity_error:.12e}"
    )

    assert relative_position_error < 1e-10
    assert relative_velocity_error < 1e-10
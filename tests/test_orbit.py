import numpy as np

from orbital.physics.angular_momentum import total_angular_momentum
from orbital.physics.body import Body
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.physics.orbit import circular_orbit_state
from orbital.physics.total_energy import total_energy
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def test_circular_orbit():
    """Um planeta em velocidade orbital deve permanecer próximo da órbita."""

    star_mass = 1.989e30
    planet_mass = 5.972e24

    orbital_radius = 1.496e11

    orbital_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT * star_mass / orbital_radius
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

    initial_distance = np.linalg.norm(
        planet.position - star.position
    )

    engine.step()

    final_distance = np.linalg.norm(
        planet.position - star.position
    )

    assert np.isclose(
        final_distance,
        initial_distance,
        rtol=1e-3,
    )


def test_circular_orbit_remains_stable():
    """A órbita deve permanecer estável ao longo de aproximadamente um ano."""

    star_mass = 1.989e30
    planet_mass = 5.972e24

    orbital_radius = 1.496e11

    orbital_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT * star_mass / orbital_radius
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

    initial_distance = np.linalg.norm(
        planet.position - star.position
    )

    for _ in range(365):
        engine.step()

    final_distance = np.linalg.norm(
        planet.position - star.position
    )

    assert np.isclose(
        final_distance,
        initial_distance,
        rtol=0.05,
    )


def test_circular_orbit_has_zero_center_of_mass():
    """O sistema orbital deve ter o centro de massa na origem."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    total_mass = mass_a + mass_b

    radius_a = mass_b / total_mass * separation
    radius_b = mass_a / total_mass * separation

    position_a = np.array([-radius_a, 0.0])
    position_b = np.array([radius_b, 0.0])

    center_of_mass_position = (
        mass_a * position_a
        + mass_b * position_b
    ) / total_mass

    assert np.allclose(
        center_of_mass_position,
        np.zeros(2),
    )


def test_circular_orbit_has_zero_center_of_mass_velocity():
    """O sistema orbital deve ter velocidade do centro de massa nula."""

    from orbital.physics.orbit import circular_orbit_velocities

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    velocity_a, velocity_b = circular_orbit_velocities(
        mass_a,
        mass_b,
        separation,
    )

    total_momentum = (
        mass_a * np.array([0.0, -velocity_a])
        + mass_b * np.array([0.0, velocity_b])
    )

    assert np.allclose(
        total_momentum,
        np.zeros(2),
    )


def test_circular_orbit_preserves_requested_separation():
    """A distância inicial entre os corpos deve ser a solicitada."""

    from orbital.physics.orbit import circular_orbit_velocities

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    circular_orbit_velocities(
        mass_a,
        mass_b,
        separation,
    )

    total_mass = mass_a + mass_b

    radius_a = mass_b / total_mass * separation
    radius_b = mass_a / total_mass * separation

    position_a = np.array([-radius_a, 0.0])
    position_b = np.array([radius_b, 0.0])

    actual_separation = np.linalg.norm(
        position_b - position_a
    )

    assert np.isclose(
        actual_separation,
        separation,
    )


def test_circular_orbit_state_has_zero_center_of_mass():
    """O estado orbital deve possuir centro de massa na origem."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    position_a, _, position_b, _ = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    total_mass = mass_a + mass_b

    center_of_mass = (
        mass_a * position_a
        + mass_b * position_b
    ) / total_mass

    assert np.allclose(
        center_of_mass,
        np.zeros(2),
    )


def test_circular_orbit_state_has_zero_center_of_mass_velocity():
    """O estado orbital deve possuir velocidade do CM igual a zero."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    _, velocity_a, _, velocity_b = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    total_momentum = (
        mass_a * velocity_a
        + mass_b * velocity_b
    )

    assert np.allclose(
        total_momentum,
        np.zeros(2),
    )


def test_circular_orbit_state_preserves_separation():
    """A configuração deve manter a separação solicitada."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    position_a, _, position_b, _ = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    actual_separation = np.linalg.norm(
        position_b - position_a
    )

    assert np.isclose(
        actual_separation,
        separation,
    )


def test_two_body_circular_orbit_remains_stable():
    """Uma órbita circular de dois corpos deve permanecer estável."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    (
        position_a,
        velocity_a,
        position_b,
        velocity_b,
    ) = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    body_a = Body(
        mass=mass_a,
        position=position_a,
        velocity=velocity_a,
        radius=1.0,
    )

    body_b = Body(
        mass=mass_b,
        position=position_b,
        velocity=velocity_b,
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body_a, body_b],
    )

    engine = SimulationEngine(
        state=state,
        dt=86400.0,
    )

    initial_separation = np.linalg.norm(
        body_b.position - body_a.position
    )

    for _ in range(365):
        engine.step()

    final_separation = np.linalg.norm(
        body_b.position - body_a.position
    )

    assert np.isclose(
        final_separation,
        initial_separation,
        rtol=0.05,
    )


def test_two_body_circular_orbit_conserves_energy():
    """A energia mecânica deve permanecer aproximadamente constante."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    (
        position_a,
        velocity_a,
        position_b,
        velocity_b,
    ) = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    body_a = Body(
        mass=mass_a,
        position=position_a,
        velocity=velocity_a,
        radius=1.0,
    )

    body_b = Body(
        mass=mass_b,
        position=position_b,
        velocity=velocity_b,
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body_a, body_b],
    )

    engine = SimulationEngine(
        state=state,
        dt=86400.0,
    )

    initial_energy = total_energy(state.bodies)

    for _ in range(365):
        engine.step()

    final_energy = total_energy(state.bodies)

    relative_error = abs(
        (final_energy - initial_energy)
        / initial_energy
    )

    assert relative_error < 1e-3


def test_two_body_circular_orbit_conserves_angular_momentum():
    """O momento angular deve permanecer aproximadamente constante."""

    mass_a = 2.0e30
    mass_b = 1.0e30
    separation = 1.0e11

    (
        position_a,
        velocity_a,
        position_b,
        velocity_b,
    ) = circular_orbit_state(
        mass_a,
        mass_b,
        separation,
    )

    body_a = Body(
        mass=mass_a,
        position=position_a,
        velocity=velocity_a,
        radius=1.0,
    )

    body_b = Body(
        mass=mass_b,
        position=position_b,
        velocity=velocity_b,
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body_a, body_b],
    )

    engine = SimulationEngine(
        state=state,
        dt=86400.0,
    )

    initial_angular_momentum = total_angular_momentum(
        state.bodies
    )

    for _ in range(365):
        engine.step()

    final_angular_momentum = total_angular_momentum(
        state.bodies
    )

    relative_error = abs(
        (final_angular_momentum - initial_angular_momentum)
        / initial_angular_momentum
    )

    assert relative_error < 1e-10
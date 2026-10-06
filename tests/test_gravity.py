import numpy as np

from orbital.physics.body import Body
from orbital.physics.gravity import (
    GRAVITATIONAL_CONSTANT,
    gravitational_acceleration,
)


def test_gravitational_acceleration_magnitude():
    """Verifica a magnitude da aceleração gravitacional."""

    source = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    target = Body(
        mass=1.0,
        position=np.array([1.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    acceleration = gravitational_acceleration(source, target)

    expected = GRAVITATIONAL_CONSTANT

    assert np.isclose(acceleration[0], -expected)
    assert np.isclose(acceleration[1], 0.0)


def test_gravitational_acceleration_direction():
    """A aceleração deve apontar em direção ao corpo-fonte."""

    source = Body(
        mass=10.0,
        position=np.array([5.0, 5.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    target = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    acceleration = gravitational_acceleration(source, target)

    assert acceleration[0] > 0
    assert acceleration[1] > 0

def test_earth_surface_gravity():
    """Verifica se a gravidade calculada se aproxima da gravidade terrestre."""

    earth = Body(
        mass=5.972e24,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=6.371e6,
    )

    surface_point = Body(
        mass=1.0,
        position=np.array([6.371e6, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    acceleration = gravitational_acceleration(earth, surface_point)

    expected_gravity = 9.81

    assert np.isclose(
        np.linalg.norm(acceleration),
        expected_gravity,
        rtol=0.01,
    )
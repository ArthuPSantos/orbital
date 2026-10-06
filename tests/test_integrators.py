import numpy as np

from orbital.physics.velocity_verlet import VelocityVerlet


def test_velocity_verlet_constant_acceleration():
    """Verifica o movimento sob aceleração constante."""

    integrator = VelocityVerlet()

    position = np.array([0.0, 0.0])
    velocity = np.array([10.0, 0.0])
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
        np.array([11.0, 0.0]),
    )

    assert np.allclose(
        result.velocity,
        np.array([12.0, 0.0]),
    )

    assert np.allclose(
        result.acceleration,
        np.array([2.0, 0.0]),
    )


def test_velocity_verlet_gravitational_fall():
    """Verifica um pequeno passo de queda sob gravidade constante."""

    integrator = VelocityVerlet()

    position = np.array([0.0, 100.0])
    velocity = np.array([0.0, 0.0])
    acceleration = np.array([0.0, -9.81])

    def acceleration_function(position):
        return np.array([0.0, -9.81])

    result = integrator.step(
        position=position,
        velocity=velocity,
        acceleration=acceleration,
        acceleration_function=acceleration_function,
        dt=1.0,
    )

    assert np.allclose(
        result.position,
        np.array([0.0, 95.095]),
    )

    assert np.allclose(
        result.velocity,
        np.array([0.0, -9.81]),
    )

    assert np.allclose(
        result.acceleration,
        np.array([0.0, -9.81]),
    )
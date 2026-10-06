import numpy as np

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.physics.gravity_solver import GravitySolver


def test_gravity_solver_uses_provided_positions():
    """O solver deve calcular a gravidade usando as posições fornecidas."""

    positions = np.array([
        [0.0, 0.0],
        [200.0, 0.0],
    ])

    masses = np.array([
        1.0e10,
        1.0,
    ])

    solver = GravitySolver()

    accelerations = solver.calculate_accelerations(
        positions,
        masses,
    )

    expected = (
        GRAVITATIONAL_CONSTANT
        * masses[0]
        / 200.0**2
    )

    assert np.isclose(
        accelerations[1][0],
        -expected,
    )

    assert np.isclose(
        accelerations[1][1],
        0.0,
    )
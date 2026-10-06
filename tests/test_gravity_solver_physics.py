import numpy as np

from orbital.physics.gravity_solver import GravitySolver


def test_gravity_solver_conserves_internal_momentum():
    """
    As forças gravitacionais internas devem se cancelar.

    Pela terceira lei de Newton, a força exercida por A em B
    deve ser igual e oposta à força exercida por B em A.
    """

    positions = np.array([
        [-1.0e10, 0.0],
        [1.0e10, 0.0],
        [0.0, 1.5e10],
    ])

    masses = np.array([
        2.0e24,
        3.0e24,
        4.0e24,
    ])

    solver = GravitySolver()

    accelerations = solver.calculate_accelerations(
        positions,
        masses,
    )

    total_force = np.sum(
        masses[:, np.newaxis] * accelerations,
        axis=0,
    )

    assert np.allclose(
        total_force,
        np.zeros(2),
        rtol=1e-12,
        atol=1e12,
    )
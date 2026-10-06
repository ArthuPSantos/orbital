import numpy as np
import pytest

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.physics.gravity_solver import GravitySolver


def reference_accelerations(
    positions: np.ndarray,
    masses: np.ndarray,
) -> np.ndarray:
    """Calcula acelerações usando uma implementação simples de referência."""

    accelerations = np.zeros_like(
        positions,
        dtype=float,
    )

    for i in range(len(positions)):
        for j in range(len(positions)):
            if i == j:
                continue

            displacement = (
                positions[j]
                - positions[i]
            )

            distance_squared = np.dot(
                displacement,
                displacement,
            )

            distance = np.sqrt(
                distance_squared
            )

            accelerations[i] += (
                GRAVITATIONAL_CONSTANT
                * masses[j]
                * displacement
                / distance**3
            )

    return accelerations


def test_gravity_solver_matches_reference():
    """O solver deve produzir o mesmo resultado da implementação de referência."""

    positions = np.array([
        [-1.0e11, 2.0e10],
        [1.5e11, -3.0e10],
        [4.0e10, 1.2e11],
        [-8.0e10, -9.0e10],
    ])

    masses = np.array([
        1.989e30,
        5.972e24,
        6.39e23,
        7.35e22,
    ])

    expected = reference_accelerations(
        positions,
        masses,
    )

    solver = GravitySolver()

    actual = solver.calculate_accelerations(
        positions,
        masses,
    )

    assert np.allclose(
        actual,
        expected,
        rtol=1e-12,
        atol=1e-20,
    )


def generate_system(
    number_of_bodies: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Gera um sistema gravitacional determinístico para os testes."""

    rng = np.random.default_rng(42)

    positions = rng.uniform(
        -1.0e11,
        1.0e11,
        size=(number_of_bodies, 2),
    )

    masses = rng.uniform(
        1.0e20,
        1.0e30,
        size=number_of_bodies,
    )

    return positions, masses

@pytest.mark.parametrize(
    "number_of_bodies",
    [2, 5, 10, 25, 50],
)
@pytest.mark.parametrize(
    "block_size",
    [1, 2, 8, 16, 64],
)
def test_gravity_solver_block_sizes_match_reference(
    number_of_bodies: int,
    block_size: int,
) -> None:
    """Todos os tamanhos de bloco devem produzir o mesmo resultado."""

    positions, masses = generate_system(
        number_of_bodies
    )

    expected = reference_accelerations(
        positions,
        masses,
    )

    solver = GravitySolver(
        block_size=block_size
    )

    result = solver.calculate_accelerations(
        positions,
        masses,
    )

    np.testing.assert_allclose(
        result,
        expected,
        rtol=1e-12,
        atol=1e-20,
    )
import numpy as np
import pytest

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.physics.gravity_solver import GravitySolver


def test_gravity_solver_calculates_acceleration():
    """O solver deve calcular corretamente a aceleração gravitacional."""

    positions = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
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
    )

    assert np.isclose(
        accelerations[1][0],
        -expected,
    )

    assert np.isclose(
        accelerations[1][1],
        0.0,
    )


def test_gravity_solver_supports_custom_positions():
    """O solver deve calcular usando as posições fornecidas."""

    positions = np.array([
        [0.0, 0.0],
        [2.0, 0.0],
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
        / 4.0
    )

    assert np.isclose(
        accelerations[1][0],
        -expected,
    )


def test_gravity_solver_rejects_invalid_position_count():
    """A quantidade de posições deve corresponder à quantidade de massas."""

    positions = np.array([
        [0.0, 0.0],
    ])

    masses = np.array([
        1.0,
        1.0,
    ])

    solver = GravitySolver()

    with pytest.raises(ValueError):
        solver.calculate_accelerations(
            positions,
            masses,
        )

def test_gravity_solver_block_size_one() -> None:
    """O solver deve funcionar processando um corpo por bloco."""

    positions = np.array(
        [
            [0.0, 0.0],
            [1.0e10, 0.0],
            [0.0, 2.0e10],
        ]
    )

    masses = np.array(
        [
            1.0e30,
            1.0e20,
            2.0e20,
        ]
    )

    solver = GravitySolver(
        block_size=1
    )

    result = solver.calculate_accelerations(
        positions,
        masses,
    )

    assert result.shape == (3, 2)
    assert np.all(np.isfinite(result))


def test_gravity_solver_block_size_larger_than_system() -> None:
    """Um bloco maior que o sistema deve funcionar normalmente."""

    positions = np.array(
        [
            [0.0, 0.0],
            [1.0e10, 0.0],
            [0.0, 2.0e10],
        ]
    )

    masses = np.array(
        [
            1.0e30,
            1.0e20,
            2.0e20,
        ]
    )

    solver = GravitySolver(
        block_size=1000
    )

    result = solver.calculate_accelerations(
        positions,
        masses,
    )

    assert result.shape == (3, 2)
    assert np.all(np.isfinite(result))


def test_gravity_solver_rejects_invalid_block_size() -> None:
    """O solver deve rejeitar tamanhos de bloco inválidos."""

    with pytest.raises(ValueError):
        GravitySolver(block_size=0)

    with pytest.raises(ValueError):
        GravitySolver(block_size=-1)

    with pytest.raises(ValueError):
        GravitySolver(block_size=1.5)
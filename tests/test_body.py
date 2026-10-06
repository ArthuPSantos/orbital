import numpy as np
import pytest

from orbital.physics.body import Body


def test_body_creation():
    """Um corpo válido deve ser criado corretamente."""

    body = Body(
        mass=5.972e24,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=6.371e6,
    )

    assert body.mass == 5.972e24
    assert np.array_equal(body.position, [0.0, 0.0])
    assert np.array_equal(body.velocity, [0.0, 0.0])
    assert body.radius == 6.371e6


def test_body_rejects_invalid_mass():
    """A massa deve ser positiva e finita."""

    with pytest.raises(ValueError):
        Body(
            mass=0,
            position=np.array([0.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
            radius=1.0,
        )


def test_body_rejects_invalid_position():
    """A posição deve possuir duas componentes."""

    with pytest.raises(ValueError):
        Body(
            mass=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
            radius=1.0,
        )


def test_body_copies_position_and_velocity():
    """O Body deve manter cópias independentes dos arrays recebidos."""

    position = np.array([1.0, 2.0])
    velocity = np.array([3.0, 4.0])

    body = Body(
        mass=1.0,
        position=position,
        velocity=velocity,
        radius=1.0,
    )

    position[0] = 999.0
    velocity[0] = 999.0

    assert np.array_equal(
        body.position,
        [1.0, 2.0],
    )

    assert np.array_equal(
        body.velocity,
        [3.0, 4.0],
    )
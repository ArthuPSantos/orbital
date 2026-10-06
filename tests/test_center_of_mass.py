import numpy as np
import pytest

from orbital.physics.body import Body
from orbital.physics.center_of_mass import center_of_mass


def test_center_of_mass():
    """O centro de massa deve ser a média ponderada pelas massas."""

    body_a = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=3.0,
        position=np.array([4.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    result = center_of_mass([body_a, body_b])

    expected = np.array([3.0, 0.0])

    assert np.allclose(result, expected)


def test_center_of_mass_rejects_empty_system():
    """Um sistema vazio não possui centro de massa."""

    with pytest.raises(ValueError):
        center_of_mass([])
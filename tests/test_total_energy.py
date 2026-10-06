import numpy as np
import pytest

from orbital.physics.body import Body
from orbital.physics.energy import gravitational_potential_energy
from orbital.physics.total_energy import total_energy


def test_total_energy_with_single_body():
    """A energia total de um corpo isolado deve ser sua energia cinética."""

    body = Body(
        mass=2.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([3.0, 4.0]),
        radius=1.0,
    )

    assert total_energy([body]) == 25.0


def test_total_energy_with_two_bodies():
    """A energia total deve incluir energia cinética e potencial."""

    body_a = Body(
        mass=2.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=3.0,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    expected = gravitational_potential_energy(
        body_a,
        body_b,
    )

    assert np.isclose(
        total_energy([body_a, body_b]),
        expected,
    )


def test_total_energy_counts_each_pair_once():
    """A energia potencial de cada par deve ser contabilizada apenas uma vez."""

    body_a = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=1.0,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_c = Body(
        mass=1.0,
        position=np.array([0.0, 10.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    expected = (
        gravitational_potential_energy(body_a, body_b)
        + gravitational_potential_energy(body_a, body_c)
        + gravitational_potential_energy(body_b, body_c)
    )

    assert np.isclose(
        total_energy([body_a, body_b, body_c]),
        expected,
    )


def test_total_energy_with_empty_system():
    """Um sistema vazio deve possuir energia total igual a zero."""

    assert total_energy([]) == 0.0
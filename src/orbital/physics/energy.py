import numpy as np

from orbital.physics.body import Body
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT


def kinetic_energy(body: Body) -> float:
    """
    Calcula a energia cinética de um corpo.

    Args:
        body: Corpo físico.

    Returns:
        Energia cinética em joules.
    """

    speed_squared = np.dot(
        body.velocity,
        body.velocity,
    )

    return 0.5 * body.mass * speed_squared


def gravitational_potential_energy(
    body_a: Body,
    body_b: Body,
) -> float:
    """
    Calcula a energia potencial gravitacional entre dois corpos.

    Args:
        body_a: Primeiro corpo.
        body_b: Segundo corpo.

    Returns:
        Energia potencial gravitacional em joules.

    Raises:
        ValueError: Se os corpos ocuparem a mesma posição.
    """

    displacement = body_a.position - body_b.position

    distance_squared = np.dot(
        displacement,
        displacement,
    )

    if distance_squared == 0:
        raise ValueError(
            "Não é possível calcular a energia potencial "
            "entre corpos na mesma posição."
        )

    distance = np.sqrt(distance_squared)

    return (
        -GRAVITATIONAL_CONSTANT
        * body_a.mass
        * body_b.mass
        / distance
    )
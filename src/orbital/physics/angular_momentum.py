import numpy as np

from orbital.physics.body import Body
from orbital.physics.center_of_mass import center_of_mass


def center_of_mass_velocity(bodies: list[Body]) -> np.ndarray:
    """
    Calcula a velocidade do centro de massa.

    Args:
        bodies: Corpos pertencentes ao sistema.

    Returns:
        Velocidade do centro de massa [vx, vy].

    Raises:
        ValueError: Se a lista de corpos estiver vazia.
    """

    if not bodies:
        raise ValueError(
            "Não é possível calcular a velocidade do centro de massa "
            "de um sistema vazio."
        )

    total_mass = sum(body.mass for body in bodies)

    weighted_velocities = sum(
        (
            body.mass * body.velocity
            for body in bodies
        ),
        start=np.zeros(2, dtype=float),
    )

    return weighted_velocities / total_mass


def total_angular_momentum(bodies: list[Body]) -> float:
    """
    Calcula o momento angular total em relação ao centro de massa.

    Args:
        bodies: Corpos pertencentes ao sistema.

    Returns:
        Momento angular total em kg·m²/s.

    Raises:
        ValueError: Se a lista de corpos estiver vazia.
    """

    if not bodies:
        raise ValueError(
            "Não é possível calcular o momento angular "
            "de um sistema vazio."
        )

    center_position = center_of_mass(bodies)
    center_velocity = center_of_mass_velocity(bodies)

    total = 0.0

    for body in bodies:
        relative_position = body.position - center_position
        relative_velocity = body.velocity - center_velocity

        x, y = relative_position
        vx, vy = relative_velocity

        total += body.mass * (x * vy - y * vx)

    return total


def angular_momentum(body: Body) -> float:
    """
    Calcula o momento angular de um corpo em relação à origem.

    Esta função é mantida para cálculos individuais.
    Para sistemas físicos, prefira `total_angular_momentum`.
    """

    x, y = body.position
    vx, vy = body.velocity

    return body.mass * (x * vy - y * vx)
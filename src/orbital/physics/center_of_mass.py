import numpy as np

from orbital.physics.body import Body


def center_of_mass(bodies: list[Body]) -> np.ndarray:
    """
    Calcula a posição do centro de massa de um sistema.

    Args:
        bodies: Corpos pertencentes ao sistema.

    Returns:
        Posição do centro de massa [x, y].

    Raises:
        ValueError: Se a lista de corpos estiver vazia.
    """

    if not bodies:
        raise ValueError(
            "Não é possível calcular o centro de massa "
            "de um sistema vazio."
        )

    total_mass = sum(body.mass for body in bodies)

    weighted_positions = sum(
        (
            body.mass * body.position
            for body in bodies
        ),
        start=np.zeros(2, dtype=float),
    )

    return weighted_positions / total_mass
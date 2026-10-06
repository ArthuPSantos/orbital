import numpy as np

from orbital.physics.body import Body

# Constante gravitacional universal.
# Unidade: m³ kg⁻¹ s⁻²
GRAVITATIONAL_CONSTANT = 6.67430e-11


def gravitational_acceleration(source: Body, target: Body) -> np.ndarray:
    """
    Calcula a aceleração gravitacional exercida por `source` sobre `target`.

    Args:
        source: Corpo que exerce a força gravitacional.
        target: Corpo que sofre a influência gravitacional.

    Returns:
        Vetor de aceleração [ax, ay] em m/s².

    Raises:
        ValueError: Se os corpos ocuparem exatamente a mesma posição.
    """

    displacement = source.position - target.position
    distance_squared = np.dot(displacement, displacement)

    if distance_squared == 0:
        raise ValueError(
            "Não é possível calcular a gravidade entre corpos "
            "que ocupam a mesma posição."
        )

    distance = np.sqrt(distance_squared)

    return (
        GRAVITATIONAL_CONSTANT
        * source.mass
        * displacement
        / distance**3
    )
import numpy as np

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT


def circular_orbit_velocities(
    mass_a: float,
    mass_b: float,
    separation: float,
) -> tuple[float, float]:
    """
    Calcula as velocidades orbitais de dois corpos em uma órbita circular.

    Os corpos orbitam o centro de massa do sistema.

    Args:
        mass_a: Massa do primeiro corpo em kg.
        mass_b: Massa do segundo corpo em kg.
        separation: Distância entre os centros dos dois corpos em metros.

    Returns:
        Tupla contendo as velocidades orbitais dos corpos em m/s.

    Raises:
        ValueError: Se as massas ou a separação forem inválidas.
    """

    if not np.isfinite(mass_a) or mass_a <= 0:
        raise ValueError("A massa A deve ser maior que zero.")

    if not np.isfinite(mass_b) or mass_b <= 0:
        raise ValueError("A massa B deve ser maior que zero.")

    if not np.isfinite(separation) or separation <= 0:
        raise ValueError("A separação deve ser maior que zero.")

    total_mass = mass_a + mass_b

    angular_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT
        * total_mass
        / separation**3
    )

    radius_a = (
        mass_b
        / total_mass
        * separation
    )

    radius_b = (
        mass_a
        / total_mass
        * separation
    )

    velocity_a = angular_velocity * radius_a
    velocity_b = angular_velocity * radius_b

    return velocity_a, velocity_b


def circular_orbit_state(
    mass_a: float,
    mass_b: float,
    separation: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Cria o estado inicial de uma órbita circular de dois corpos.

    O centro de massa e a velocidade do centro de massa ficam
    na origem e iguais a zero.

    Args:
        mass_a: Massa do primeiro corpo em kg.
        mass_b: Massa do segundo corpo em kg.
        separation: Distância entre os corpos em metros.

    Returns:
        Tupla contendo:
            position_a: Posição do corpo A.
            velocity_a: Velocidade do corpo A.
            position_b: Posição do corpo B.
            velocity_b: Velocidade do corpo B.

    Raises:
        ValueError: Se as massas ou a separação forem inválidas.
    """

    velocity_a, velocity_b = circular_orbit_velocities(
        mass_a,
        mass_b,
        separation,
    )

    total_mass = mass_a + mass_b

    radius_a = (
        mass_b
        / total_mass
        * separation
    )

    radius_b = (
        mass_a
        / total_mass
        * separation
    )

    position_a = np.array(
        [-radius_a, 0.0],
        dtype=float,
    )

    position_b = np.array(
        [radius_b, 0.0],
        dtype=float,
    )

    velocity_vector_a = np.array(
        [0.0, -velocity_a],
        dtype=float,
    )

    velocity_vector_b = np.array(
        [0.0, velocity_b],
        dtype=float,
    )

    return (
        position_a,
        velocity_vector_a,
        position_b,
        velocity_vector_b,
    )
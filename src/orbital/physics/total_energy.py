
from orbital.physics.body import Body
from orbital.physics.energy import (
    gravitational_potential_energy,
    kinetic_energy,
)


def total_energy(bodies: list[Body]) -> float:
    """
    Calcula a energia mecânica total de um sistema.

    A energia total é composta pela soma da energia cinética
    de todos os corpos e da energia potencial gravitacional
    entre cada par de corpos.

    Args:
        bodies: Corpos pertencentes ao sistema.

    Returns:
        Energia mecânica total em joules.
    """

    kinetic = sum(
        kinetic_energy(body)
        for body in bodies
    )

    potential = 0.0

    for i, body_a in enumerate(bodies):
        for body_b in bodies[i + 1:]:
            potential += gravitational_potential_energy(
                body_a,
                body_b,
            )

    return kinetic + potential
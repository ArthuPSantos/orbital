
import numpy as np

from orbital.physics.body import Body
from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def simulate_orbit(steps_per_orbit: int) -> float:
    """
    Simula uma órbita circular de dois corpos em torno do
    centro de massa e retorna o erro relativo de fechamento.

    A condição inicial é construída de forma fisicamente consistente:

        v_rel = sqrt(G * (M1 + M2) / r)

    O período analítico é:

        T = 2*pi*sqrt(r³ / (G * (M1 + M2)))

    Assim, cada resolução executa exatamente uma órbita.
    """

    star_mass = 1.989e30
    planet_mass = 5.972e24

    separation = 1.496e11

    total_mass = star_mass + planet_mass

    # Velocidade relativa necessária para uma órbita circular.
    relative_velocity = np.sqrt(
        GRAVITATIONAL_CONSTANT
        * total_mass
        / separation
    )

    # Período orbital analítico.
    orbital_period = 2.0 * np.pi * np.sqrt(
        separation**3
        / (
            GRAVITATIONAL_CONSTANT
            * total_mass
        )
    )

    dt = orbital_period / steps_per_orbit

    # Posições em relação ao centro de massa.
    star_position = np.array([
        -planet_mass / total_mass * separation,
        0.0,
    ])

    planet_position = np.array([
        star_mass / total_mass * separation,
        0.0,
    ])

    # Velocidades em relação ao centro de massa.
    star_velocity = np.array([
        0.0,
        -planet_mass / total_mass * relative_velocity,
    ])

    planet_velocity = np.array([
        0.0,
        star_mass / total_mass * relative_velocity,
    ])

    star = Body(
        mass=star_mass,
        position=star_position,
        velocity=star_velocity,
        radius=6.9634e8,
    )

    planet = Body(
        mass=planet_mass,
        position=planet_position,
        velocity=planet_velocity,
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[star, planet],
    )

    engine = SimulationEngine(
        state=state,
        dt=dt,
    )

    initial_relative_position = (
        planet.position - star.position
    ).copy()

    for _ in range(steps_per_orbit):
        engine.step()

    final_relative_position = (
        planet.position - star.position
    )

    closure_error = np.linalg.norm(
        final_relative_position
        - initial_relative_position
    )

    return closure_error / separation


def test_velocity_verlet_is_second_order():
    """
    Verifica experimentalmente a ordem de convergência
    do integrador Velocity Verlet.

    Para um método de segunda ordem:

        erro ∝ dt²

    Ao dobrarmos o número de passos, o dt é reduzido
    pela metade e o erro deve cair aproximadamente
    por um fator de quatro.
    """

    error_500 = simulate_orbit(500)
    error_1000 = simulate_orbit(1000)
    error_2000 = simulate_orbit(2000)

    ratio_1 = error_500 / error_1000
    ratio_2 = error_1000 / error_2000

    print(f"Erro com 500 passos:  {error_500:.12e}")
    print(f"Erro com 1000 passos: {error_1000:.12e}")
    print(f"Erro com 2000 passos: {error_2000:.12e}")

    print(f"Razão 500/1000:  {ratio_1:.6f}")
    print(f"Razão 1000/2000: {ratio_2:.6f}")

    assert 3.0 < ratio_1 < 5.0
    assert 3.0 < ratio_2 < 5.0


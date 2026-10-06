"""
Experimento de convergência numérica do ORBITAL.

Este experimento compara diferentes tamanhos de passo DT
contra uma solução de referência calculada com um DT muito
menor.

O objetivo é verificar se a solução numérica converge para
uma solução mais precisa conforme DT diminui.
"""

import matplotlib.pyplot as plt
import numpy as np

from orbital.physics.body import Body
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState

SECONDS_PER_DAY = 86_400

STAR_MASS = 1.989e30
PLANET_MASS = 5.972e24

STAR_POSITION = np.array(
    [0.0, 0.0],
    dtype=float,
)

PLANET_POSITION = np.array(
    [1.496e11, 0.0],
    dtype=float,
)

STAR_VELOCITY = np.array(
    [0.0, 0.0],
    dtype=float,
)

PLANET_VELOCITY = np.array(
    [0.0, 29_780.0],
    dtype=float,
)

SIMULATION_DAYS = 365

DT_VALUES = [
    86_400.0,
    43_200.0,
    21_600.0,
    10_800.0,
    5_400.0,
    2_700.0,
]

REFERENCE_DT = 1_350.0


def create_engine(dt: float) -> SimulationEngine:
    """
    Cria uma nova simulação de dois corpos.

    Args:
        dt: Intervalo de integração em segundos.

    Returns:
        Engine configurado com as condições iniciais do experimento.
    """

    star = Body(
        mass=STAR_MASS,
        position=STAR_POSITION.copy(),
        velocity=STAR_VELOCITY.copy(),
        radius=6.9634e8,
    )

    planet = Body(
        mass=PLANET_MASS,
        position=PLANET_POSITION.copy(),
        velocity=PLANET_VELOCITY.copy(),
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[star, planet],
    )

    return SimulationEngine(
        state=state,
        dt=dt,
    )


def run_simulation(dt: float) -> np.ndarray:
    """
    Executa uma simulação e retorna a posição final do planeta.

    Args:
        dt: Intervalo de integração em segundos.

    Returns:
        Vetor contendo a posição final do planeta.
    """

    simulation_seconds = (
        SIMULATION_DAYS
        * SECONDS_PER_DAY
    )

    steps = int(
        simulation_seconds / dt
    )

    engine = create_engine(dt)

    for _ in range(steps):
        engine.step()

    planet = engine.state.bodies[1]

    return planet.position.copy()


def calculate_relative_position_error(
    position: np.ndarray,
    reference_position: np.ndarray,
) -> float:
    """
    Calcula o erro relativo da posição em relação à referência.

    Args:
        position: Posição final da simulação avaliada.
        reference_position: Posição final da simulação de referência.

    Returns:
        Erro relativo da posição.
    """

    absolute_error = np.linalg.norm(
        position - reference_position,
    )

    reference_norm = np.linalg.norm(
        reference_position,
    )

    return absolute_error / reference_norm


def plot_convergence(
    results: list[tuple[float, int, float]],
) -> None:
    """
    Exibe o erro relativo da posição em função de DT.

    Ambos os eixos utilizam escala logarítmica para facilitar
    a visualização da convergência.

    Args:
        results: Resultados do experimento.
    """

    dt_values = np.array(
        [result[0] for result in results],
    )

    errors = np.array(
        [result[2] for result in results],
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        dt_values,
        errors,
        marker="o",
        label="Erro relativo da posição",
    )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Intervalo DT (s)")
    plt.ylabel("Erro relativo da posição")
    plt.title("ORBITAL — Convergência Numérica")

    plt.grid(True, which="both", alpha=0.3)
    plt.legend()

    plt.show()


def main() -> None:
    """
    Executa o experimento de convergência e exibe os resultados.
    """

    print("=" * 70)
    print("ORBITAL — EXPERIMENTO DE CONVERGÊNCIA NUMÉRICA")
    print("=" * 70)

    print("\nCONFIGURAÇÃO")
    print("-" * 70)

    print(
        f"Duração da simulação: "
        f"{SIMULATION_DAYS} dias"
    )

    print(
        f"DT de referência: "
        f"{REFERENCE_DT:.0f} segundos"
    )

    print("\nCalculando solução de referência...")

    reference_position = run_simulation(
        REFERENCE_DT,
    )

    results: list[tuple[float, int, float]] = []

    for dt in DT_VALUES:
        position = run_simulation(dt)

        steps = int(
            SIMULATION_DAYS
            * SECONDS_PER_DAY
            / dt
        )

        error = calculate_relative_position_error(
            position,
            reference_position,
        )

        results.append(
            (
                dt,
                steps,
                error,
            )
        )

    print("\nRESULTADOS")
    print("-" * 70)

    print(
        f"{'DT (s)':>12}"
        f"{'Passos':>15}"
        f"{'Erro posição':>25}"
    )

    for dt, steps, error in results:
        print(
            f"{dt:>12.0f}"
            f"{steps:>15}"
            f"{error:>25.6e}"
        )

    print("\n" + "=" * 70)

    plot_convergence(results)


if __name__ == "__main__":
    main()
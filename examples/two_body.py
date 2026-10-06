"""
Experimento de dois corpos do ORBITAL.

Este arquivo contém a lógica de execução do experimento.

Os parâmetros configuráveis ficam separados em:

    two_body_config.py

Dessa forma, podemos alterar as condições iniciais sem
modificar o código responsável pela simulação.
"""

import numpy as np
from two_body_config import (
    DT,
    ENERGY_SAMPLE_DAYS,
    PLANET_MASS,
    PLANET_POSITION,
    PLANET_VELOCITY,
    SIMULATION_DAYS,
    STAR_MASS,
    STAR_POSITION,
    STAR_VELOCITY,
)

from orbital.physics.body import Body
from orbital.physics.total_energy import total_energy
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState

SECONDS_PER_DAY = 86_400


def run_experiment() -> dict[str, object]:
    """
    Executa o experimento de dois corpos.

    Retorna os principais resultados da simulação para que
    outras partes do projeto possam utilizá-los sem precisar
    executar novamente toda a lógica.

    Returns:
        Dicionário contendo:
            - estado final da simulação;
            - histórico de energia;
            - histórico de tempo;
            - trajetória da estrela;
            - trajetória do planeta;
            - energia inicial;
            - energia final;
            - erro relativo de energia;
            - distância entre posição inicial e final;
            - número de passos executados.
    """

    simulation_seconds = (
        SIMULATION_DAYS
        * SECONDS_PER_DAY
    )

    energy_sample_seconds = (
        ENERGY_SAMPLE_DAYS
        * SECONDS_PER_DAY
    )

    if simulation_seconds % DT != 0:
        raise ValueError(
            "DT deve dividir exatamente a duração da simulação. "
            "Altere SIMULATION_DAYS ou DT no two_body_config.py."
        )

    if energy_sample_seconds % DT != 0:
        raise ValueError(
            "ENERGY_SAMPLE_DAYS deve representar uma quantidade "
            "de passos compatível com DT."
        )

    steps = int(
        simulation_seconds / DT
    )

    energy_sample_steps = int(
        energy_sample_seconds / DT
    )

    star = Body(
        mass=STAR_MASS,
        position=np.array(
            STAR_POSITION,
            dtype=float,
        ),
        velocity=np.array(
            STAR_VELOCITY,
            dtype=float,
        ),
        radius=6.9634e8,
    )

    planet = Body(
        mass=PLANET_MASS,
        position=np.array(
            PLANET_POSITION,
            dtype=float,
        ),
        velocity=np.array(
            PLANET_VELOCITY,
            dtype=float,
        ),
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[star, planet],
    )

    engine = SimulationEngine(
        state=state,
        dt=DT,
    )

    initial_position = planet.position.copy()

    initial_energy = total_energy(
        state.bodies,
    )

    energy_history: list[
        tuple[float, float, float]
    ] = [
        (
            0.0,
            initial_energy,
            0.0,
        )
    ]

    trajectory_times = [0.0]

    trajectory_star = [
        star.position.copy()
    ]

    trajectory_planet = [
        planet.position.copy()
    ]

    for step in range(1, steps + 1):

        engine.step()

        trajectory_times.append(
            state.time / SECONDS_PER_DAY
        )

        trajectory_star.append(
            star.position.copy()
        )

        trajectory_planet.append(
            planet.position.copy()
        )

        if step % energy_sample_steps == 0:

            current_energy = total_energy(
                state.bodies,
            )

            relative_error = abs(
                (current_energy - initial_energy)
                / initial_energy
            )

            current_time_days = (
                state.time
                / SECONDS_PER_DAY
            )

            energy_history.append(
                (
                    current_time_days,
                    current_energy,
                    relative_error,
                )
            )

    final_energy = total_energy(
        state.bodies,
    )

    position_difference = np.linalg.norm(
        planet.position - initial_position,
    )

    energy_relative_error = abs(
        (final_energy - initial_energy)
        / initial_energy
    )

    return {
        "state": state,
        "energy_history": energy_history,
        "trajectory_times": trajectory_times,
        "trajectory_star": trajectory_star,
        "trajectory_planet": trajectory_planet,
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "energy_relative_error": energy_relative_error,
        "position_difference": position_difference,
        "steps": steps,
    }


def print_results(results: dict[str, object]) -> None:
    """
    Exibe no terminal os resultados do experimento.

    Args:
        results: Resultados retornados por run_experiment().
    """

    state = results["state"]
    energy_history = results["energy_history"]
    initial_energy = results["initial_energy"]
    energy_relative_error = results["energy_relative_error"]
    position_difference = results["position_difference"]
    steps = results["steps"]

    print("=" * 60)
    print("ORBITAL — EXPERIMENTO DE DOIS CORPOS")
    print("=" * 60)

    print("\nCONFIGURAÇÃO")
    print("-" * 60)

    print(
        f"Duração: {SIMULATION_DAYS} dias"
    )

    print(
        f"Intervalo DT: {DT:.0f} segundos"
    )

    print(
        f"Número de passos: {steps}"
    )

    print(
        f"Amostragem de energia: "
        f"a cada {ENERGY_SAMPLE_DAYS} dias"
    )

    print("\nESTADO INICIAL")
    print("-" * 60)

    print(
        "Tempo: 0.0 dias"
    )

    print(
        "Posição do planeta:",
        PLANET_POSITION,
    )

    print(
        "Velocidade do planeta:",
        PLANET_VELOCITY,
    )

    print(
        f"Energia total: "
        f"{initial_energy:.6e} J",
    )

    print("\nHISTÓRICO DE ENERGIA")
    print("-" * 60)

    print(
        f"{'Tempo (dias)':>15}"
        f"{'Energia (J)':>25}"
        f"{'Erro relativo':>20}"
    )

    for (
        time_days,
        energy,
        relative_error,
    ) in energy_history:

        print(
            f"{time_days:>15.1f}"
            f"{energy:>25.6e}"
            f"{relative_error:>20.6e}"
        )

    print("\nRESULTADO FINAL")
    print("-" * 60)

    print(
        f"Tempo: "
        f"{state.time / SECONDS_PER_DAY:.1f} dias"
    )

    planet = state.bodies[1]

    print(
        "Posição do planeta:",
        planet.position,
    )

    print(
        "Velocidade do planeta:",
        planet.velocity,
    )

    print(
        f"Distância entre posição inicial e final: "
        f"{position_difference:.6e} m"
    )

    print(
        f"Erro relativo de energia: "
        f"{energy_relative_error:.6e}"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    results = run_experiment()
    print_results(results)
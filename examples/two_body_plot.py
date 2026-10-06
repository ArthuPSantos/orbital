"""
Visualização do experimento de dois corpos do ORBITAL.

Este arquivo utiliza os dados produzidos por run_experiment()
para visualizar a trajetória dos corpos e a conservação de
energia durante a simulação.

A física da simulação permanece separada deste módulo.
"""

import matplotlib.pyplot as plt
import numpy as np
from two_body import run_experiment

ASTRONOMICAL_UNIT = 1.496e11


def plot_trajectory(results: dict[str, object]) -> None:
    """
    Exibe a trajetória dos corpos no plano XY.

    As posições são convertidas de metros para unidades
    astronômicas (UA) para facilitar a interpretação visual.

    Args:
        results: Resultados retornados por run_experiment().
    """

    trajectory_star = (
        np.array(results["trajectory_star"])
        / ASTRONOMICAL_UNIT
    )

    trajectory_planet = (
        np.array(results["trajectory_planet"])
        / ASTRONOMICAL_UNIT
    )

    plt.figure(figsize=(10, 10))

    plt.plot(
        trajectory_planet[:, 0],
        trajectory_planet[:, 1],
        label="Trajetória do planeta",
    )

    plt.scatter(
        trajectory_star[0, 0],
        trajectory_star[0, 1],
        s=120,
        label="Estrela",
        zorder=3,
    )

    plt.scatter(
        trajectory_planet[0, 0],
        trajectory_planet[0, 1],
        s=60,
        label="Posição inicial",
        zorder=3,
    )

    plt.scatter(
        trajectory_planet[-1, 0],
        trajectory_planet[-1, 1],
        s=60,
        label="Posição final",
        zorder=3,
    )

    plt.xlabel("Posição X (UA)")
    plt.ylabel("Posição Y (UA)")
    plt.title("ORBITAL — Trajetória do Sistema de Dois Corpos")

    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.show()


def plot_energy_error(results: dict[str, object]) -> None:
    """
    Exibe o erro relativo de energia ao longo do tempo.

    O eixo Y utiliza escala logarítmica para tornar pequenos
    erros numéricos mais fáceis de visualizar.

    Args:
        results: Resultados retornados por run_experiment().
    """

    energy_history = np.array(
        results["energy_history"],
    )

    time_days = energy_history[:, 0]
    relative_error = energy_history[:, 2]

    positive_errors = relative_error > 0

    plt.figure(figsize=(10, 6))

    plt.plot(
        time_days[positive_errors],
        relative_error[positive_errors],
        marker="o",
        label="Erro relativo de energia",
    )

    plt.xlabel("Tempo (dias)")
    plt.ylabel("Erro relativo de energia")
    plt.title("ORBITAL — Conservação de Energia")

    plt.yscale("log")

    plt.grid(True, which="both", alpha=0.3)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    results = run_experiment()

    plot_trajectory(results)
    plot_energy_error(results)
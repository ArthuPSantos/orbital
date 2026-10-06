import time

import numpy as np

from orbital.physics.gravity_solver import GravitySolver


def generate_system(
    number_of_bodies: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Gera um sistema gravitacional aleatório."""

    rng = np.random.default_rng(42)

    positions = rng.uniform(
        -1.0e11,
        1.0e11,
        size=(number_of_bodies, 2),
    )

    masses = rng.uniform(
        1.0e20,
        1.0e30,
        size=number_of_bodies,
    )

    return positions, masses


def measure(
    solver: GravitySolver,
    positions: np.ndarray,
    masses: np.ndarray,
) -> float:
    """Mede uma execução do solver em segundos."""

    start = time.perf_counter()

    solver.calculate_accelerations(
        positions,
        masses,
    )

    return time.perf_counter() - start


def main() -> None:
    """Executa o teste de escalabilidade do solver."""

    solver = GravitySolver()

    sizes = [
        5000,
        7500,
        10000,
        
    ]

    print()
    print("=" * 72)
    print("ORBITAL — TESTE DE ESCALABILIDADE DO GRAVITY SOLVER")
    print("=" * 72)
    print()
    print(
        f"{'N':>8}"
        f"{'Memória estimada':>22}"
        f"{'Tempo (s)':>15}"
    )
    print("-" * 72)

    for number_of_bodies in sizes:
        positions, masses = generate_system(
            number_of_bodies
        )

        memory_gb = (
            number_of_bodies**2
            * 2
            * 8
            / 1024**3
        )

        elapsed = measure(
            solver,
            positions,
            masses,
        )

        print(
            f"{number_of_bodies:>8}"
            f"{memory_gb:>20.2f} GB"
            f"{elapsed:>15.4f}"
        )

    print("-" * 72)
    print()


if __name__ == "__main__":
    main()
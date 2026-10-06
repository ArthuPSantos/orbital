import time

import numpy as np

from orbital.physics.gravity_solver import GravitySolver


def generate_system(
    number_of_bodies: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Gera um sistema gravitacional determinístico."""

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


def main() -> None:
    """Executa o teste de escalabilidade."""

    solver = GravitySolver(
        block_size=512
    )

    sizes = [
        12500,
        15000,
        20000,
    ]

    print()
    print("=" * 72)
    print("ORBITAL — ESCALABILIDADE DO SOLVER BLOQUEADO")
    print("=" * 72)
    print()
    print(
        f"{'N':>8}"
        f"{'Tempo (s)':>18}"
    )
    print("-" * 72)

    for number_of_bodies in sizes:
        positions, masses = generate_system(
            number_of_bodies
        )

        start = time.perf_counter()

        solver.calculate_accelerations(
            positions,
            masses,
        )

        elapsed = time.perf_counter() - start

        print(
            f"{number_of_bodies:>8}"
            f"{elapsed:>18.4f}"
        )

    print("-" * 72)
    print()


if __name__ == "__main__":
    main()
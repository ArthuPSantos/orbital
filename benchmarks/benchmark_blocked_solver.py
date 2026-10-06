import time

import numpy as np

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
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


def fully_vectorized_solver(
    positions: np.ndarray,
    masses: np.ndarray,
) -> np.ndarray:
    """Implementação totalmente vetorizada usada como referência."""

    displacement = (
        positions[np.newaxis, :, :]
        - positions[:, np.newaxis, :]
    )

    distance_squared = np.sum(
        displacement**2,
        axis=2,
    )

    np.fill_diagonal(
        distance_squared,
        1.0,
    )

    inverse_distance_cubed = (
        distance_squared ** -1.5
    )

    np.fill_diagonal(
        inverse_distance_cubed,
        0.0,
    )

    acceleration_contributions = (
        displacement
        * inverse_distance_cubed[:, :, np.newaxis]
        * masses[np.newaxis, :, np.newaxis]
    )

    return (
        GRAVITATIONAL_CONSTANT
        * np.sum(
            acceleration_contributions,
            axis=1,
        )
    )


def measure(
    function,
    positions: np.ndarray,
    masses: np.ndarray,
) -> float:
    """Mede o tempo de uma execução."""

    start = time.perf_counter()

    function(
        positions,
        masses,
    )

    return time.perf_counter() - start


def main() -> None:
    """Executa o benchmark comparativo."""

    sizes = [
        1000,
        2000,
        4000,
        5000,
        7500,
        10000,
    ]

    block_sizes = [
        128,
        256,
        512,
        1024,
    ]

    print()
    print("=" * 88)
    print("ORBITAL — BENCHMARK DO SOLVER BLOQUEADO")
    print("=" * 88)
    print()

    for number_of_bodies in sizes:
        positions, masses = generate_system(
            number_of_bodies
        )

        reference_time = measure(
            fully_vectorized_solver,
            positions,
            masses,
        )

        print(
            f"N = {number_of_bodies}"
        )
        print(
            f"Vetorizado completo: "
            f"{reference_time:.4f} s"
        )
        print()

        for block_size in block_sizes:
            solver = GravitySolver(
                block_size=block_size
            )

            blocked_time = measure(
                solver.calculate_accelerations,
                positions,
                masses,
            )

            speedup = (
                reference_time / blocked_time
            )

            print(
                f"  bloco {block_size:>4}: "
                f"{blocked_time:.4f} s"
                f"  |  {speedup:.2f}x"
            )

        print("-" * 88)


if __name__ == "__main__":
    main()
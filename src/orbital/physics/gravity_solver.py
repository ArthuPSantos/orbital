import numpy as np

from orbital.physics.gravity import GRAVITATIONAL_CONSTANT


class GravitySolver:
    """
    Calcula as acelerações gravitacionais de um sistema.

    O cálculo utiliza vetorização do NumPy em blocos.

    A complexidade computacional continua sendo O(N²), porém
    o cálculo não precisa manter todas as interações N x N
    simultaneamente na memória.

    Isso reduz significativamente o pico de memória para
    sistemas grandes, mantendo a vantagem dos cálculos
    vetorizados.
    """

    def __init__(self, block_size: int = 512) -> None:
        """
        Inicializa o solver.

        Args:
            block_size:
                Quantidade de corpos processados por bloco.
                Blocos menores reduzem o uso de memória,
                enquanto blocos maiores podem aumentar o desempenho.
        """

        if not isinstance(block_size, int) or block_size <= 0:
            raise ValueError(
                "O tamanho do bloco deve ser um inteiro maior que zero."
            )

        self.block_size = block_size

    def calculate_accelerations(
        self,
        positions: np.ndarray,
        masses: np.ndarray,
    ) -> np.ndarray:
        """
        Calcula a aceleração gravitacional de cada corpo.

        Args:
            positions:
                Matriz (N, 2) contendo as posições dos corpos.

            masses:
                Vetor (N,) contendo as massas dos corpos.

        Returns:
            Matriz (N, 2) contendo as acelerações gravitacionais.
        """

        positions = np.asarray(
            positions,
            dtype=float,
        )

        masses = np.asarray(
            masses,
            dtype=float,
        )

        if positions.ndim != 2 or positions.shape[1] != 2:
            raise ValueError(
                "As posições devem possuir formato (N, 2)."
            )

        if masses.ndim != 1:
            raise ValueError(
                "As massas devem possuir formato (N,)."
            )

        if len(positions) != len(masses):
            raise ValueError(
                "A quantidade de posições deve ser igual "
                "à quantidade de massas."
            )

        if not np.all(np.isfinite(positions)):
            raise ValueError(
                "As posições devem conter apenas valores finitos."
            )

        if not np.all(
            np.isfinite(masses)
        ) or np.any(masses <= 0):
            raise ValueError(
                "As massas devem ser valores finitos maiores que zero."
            )

        number_of_bodies = len(positions)

        accelerations = np.zeros_like(
            positions,
            dtype=float,
        )

        for start in range(
            0,
            number_of_bodies,
            self.block_size,
        ):
            end = min(
                start + self.block_size,
                number_of_bodies,
            )

            block_positions = positions[start:end]

            displacement = (
                positions[np.newaxis, :, :]
                - block_positions[:, np.newaxis, :]
            )

            distance_squared = np.sum(
                displacement**2,
                axis=2,
            )

            block_size = end - start

            local_indices = np.arange(block_size)

            global_indices = np.arange(
                start,
                end,
            )

            distance_squared[
                local_indices,
                global_indices,
            ] = 1.0

            inverse_distance_cubed = (
                distance_squared ** -1.5
            )

            inverse_distance_cubed[
                local_indices,
                global_indices,
            ] = 0.0

            acceleration_contributions = (
                displacement
                * inverse_distance_cubed[:, :, np.newaxis]
                * masses[np.newaxis, :, np.newaxis]
            )

            accelerations[start:end] = (
                GRAVITATIONAL_CONSTANT
                * np.sum(
                    acceleration_contributions,
                    axis=1,
                )
            )

        return accelerations
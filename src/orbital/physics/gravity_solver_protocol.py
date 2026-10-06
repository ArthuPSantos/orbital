from typing import Protocol

import numpy as np


class GravitySolverProtocol(Protocol):
    """
    Define o contrato para solvers gravitacionais.

    O solver recebe diretamente os dados numéricos do sistema,
    separando o cálculo gravitacional da estrutura Body.

    positions:
        Matriz com formato (N, 2), contendo a posição de cada corpo.

    masses:
        Vetor com formato (N,), contendo a massa de cada corpo.

    retorno:
        Matriz com formato (N, 2), contendo a aceleração
        gravitacional de cada corpo.
    """

    def calculate_accelerations(
        self,
        positions: np.ndarray,
        masses: np.ndarray,
    ) -> np.ndarray:
        """
        Calcula as acelerações gravitacionais do sistema.

        Args:
            positions: Posições dos corpos em metros.
            masses: Massas dos corpos em quilogramas.

        Returns:
            Acelerações dos corpos em metros por segundo ao quadrado.
        """
        ...
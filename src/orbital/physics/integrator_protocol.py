from dataclasses import dataclass
from typing import Callable, Protocol

import numpy as np


@dataclass(slots=True)
class StepResult:
    """
    Resultado de um passo de integração numérica.

    Attributes
    ----------
    position:
        Nova posição dos corpos.
    velocity:
        Nova velocidade dos corpos.
    acceleration:
        Aceleração correspondente ao novo estado.
        Pode ser None quando o integrador não a mantém em cache.
    """

    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray | None


class IntegratorProtocol(Protocol):
    """
    Contrato para integradores numéricos do ORBITAL.

    O integrador recebe o estado atual e uma função capaz de
    calcular acelerações para determinadas posições.

    Isso mantém a lógica do método numérico separada do
    mecanismo responsável pela física gravitacional.
    """

    def step(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray | None,
        acceleration_function: Callable[[np.ndarray], np.ndarray],
        dt: float,
    ) -> StepResult:
        ...
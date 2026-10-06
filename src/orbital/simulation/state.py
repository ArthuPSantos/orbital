from dataclasses import dataclass

from orbital.physics.body import Body


@dataclass(slots=True)
class SimulationState:
    """
    Representa o estado atual de uma simulação.

    Attributes:
        bodies: Corpos presentes no sistema.
        time: Tempo simulado em segundos.
    """

    bodies: list[Body]
    time: float = 0.0
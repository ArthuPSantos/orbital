from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Body:
    """
    Representa um corpo físico em uma simulação gravitacional 2D.

    Attributes:
        mass: Massa do corpo em quilogramas.
        position: Posição [x, y] em metros.
        velocity: Velocidade [vx, vy] em metros por segundo.
        radius: Raio do corpo em metros.
    """

    mass: float
    position: np.ndarray
    velocity: np.ndarray
    radius: float

    def __post_init__(self) -> None:
        """Valida os parâmetros físicos do corpo."""

        if not np.isfinite(self.mass) or self.mass <= 0:
            raise ValueError("A massa deve ser um valor finito maior que zero.")

        if not np.isfinite(self.radius) or self.radius <= 0:
            raise ValueError("O raio deve ser um valor finito maior que zero.")

        if self.position.shape != (2,):
            raise ValueError("A posição deve possuir exatamente 2 componentes.")

        if self.velocity.shape != (2,):
            raise ValueError("A velocidade deve possuir exatamente 2 componentes.")

        if not np.all(np.isfinite(self.position)):
            raise ValueError("A posição deve conter apenas valores finitos.")

        if not np.all(np.isfinite(self.velocity)):
            raise ValueError("A velocidade deve conter apenas valores finitos.")

        self.position = np.array(self.position, dtype=float, copy=True)
        self.velocity = np.array(self.velocity, dtype=float, copy=True)
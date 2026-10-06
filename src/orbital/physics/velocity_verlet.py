import numpy as np

from orbital.physics.integrator_protocol import (
    IntegratorProtocol,
    StepResult,
)


class VelocityVerlet(IntegratorProtocol):
    """
    Integrador Velocity Verlet.

    O método executa um passo completo de integração:

    1. Calcula a nova posição.
    2. Calcula a aceleração na nova posição.
    3. Calcula a nova velocidade usando a aceleração antiga
       e a nova aceleração.
    4. Retorna o novo estado junto com a aceleração calculada.

    A aceleração retornada pode ser reutilizada pelo próximo
    passo da simulação, evitando uma nova avaliação desnecessária.
    """

    def step(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray | None,
        acceleration_function,
        dt: float,
    ) -> StepResult:

        if not np.isfinite(dt) or dt <= 0:
            raise ValueError(
                "O intervalo dt deve ser um valor finito maior que zero."
            )

        if acceleration is None:
            acceleration = acceleration_function(position)

        next_position = (
            position
            + velocity * dt
            + 0.5 * acceleration * dt**2
        )

        next_acceleration = acceleration_function(
            next_position
        )

        next_velocity = (
            velocity
            + 0.5
            * (acceleration + next_acceleration)
            * dt
        )

        return StepResult(
            position=next_position,
            velocity=next_velocity,
            acceleration=next_acceleration,
        )
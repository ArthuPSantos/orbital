import numpy as np

from orbital.physics.body import Body
from orbital.physics.integrator_protocol import StepResult
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


class FakeIntegrator:
    """Integrador falso usado para testar o contrato do Engine."""

    def step(
        self,
        position,
        velocity,
        acceleration,
        acceleration_function,
        dt,
    ):
        next_position = position + velocity * dt
        next_velocity = velocity.copy()

        next_acceleration = acceleration_function(
            next_position
        )

        return StepResult(
            position=next_position,
            velocity=next_velocity,
            acceleration=next_acceleration,
        )


def test_engine_accepts_alternative_integrator():
    """O engine deve aceitar qualquer integrador compatível com o protocolo."""

    body = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([2.0, 0.0]),
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body],
    )

    integrator = FakeIntegrator()

    engine = SimulationEngine(
        state=state,
        dt=1.0,
        integrator=integrator,
    )

    engine.step()

    assert np.allclose(
        body.position,
        np.array([2.0, 0.0]),
    )

    assert np.allclose(
        body.velocity,
        np.array([2.0, 0.0]),
    )

    assert state.time == 1.0
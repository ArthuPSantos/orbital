import numpy as np

from orbital.physics.body import Body
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


class FakeGravitySolver:
    """Solver simples usado para testar a abstração do engine."""

    def calculate_accelerations(
        self,
        bodies: list[Body],
        positions: list[np.ndarray] | None = None,
    ) -> list[np.ndarray]:
        """Retorna aceleração nula para todos os corpos."""

        return [
            np.zeros(2, dtype=float)
            for _ in bodies
        ]


def test_engine_accepts_alternative_gravity_solver():
    """O engine deve aceitar qualquer solver compatível com o protocolo."""

    body = Body(
        mass=1.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([1.0, 0.0]),
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body],
    )

    solver = FakeGravitySolver()

    engine = SimulationEngine(
        state=state,
        dt=1.0,
        gravity_solver=solver,
    )

    engine.step()

    assert np.allclose(
        body.position,
        np.array([1.0, 0.0]),
    )

    assert np.allclose(
        body.velocity,
        np.array([1.0, 0.0]),
    )

    assert state.time == 1.0
import pytest
import numpy as np
from orbital.physics.body import Body
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


def test_empty_simulation_advances_time():
    """Uma simulação vazia deve continuar avançando no tempo."""

    state = SimulationState(
        bodies=[],
        time=0.0,
    )

    engine = SimulationEngine(
        state=state,
        dt=1.0,
    )

    engine.step()

    assert state.time == 1.0


def test_engine_rejects_invalid_dt():
    """O engine deve rejeitar intervalos de tempo inválidos."""

    state = SimulationState(bodies=[])

    with pytest.raises(ValueError):
        SimulationEngine(
            state=state,
            dt=0.0,
        )

def test_two_bodies_attract_each_other():
    """Dois corpos devem acelerar um em direção ao outro."""

    body_a = Body(
        mass=1.0e10,
        position=np.array([-10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=1.0e10,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body_a, body_b],
    )

    engine = SimulationEngine(
        state=state,
        dt=1.0,
    )

    initial_position_a = body_a.position.copy()
    initial_position_b = body_b.position.copy()

    engine.step()

    assert body_a.position[0] > initial_position_a[0]
    assert body_b.position[0] < initial_position_b[0]

def test_two_body_momentum_is_conserved():
    """O momento linear total deve ser conservado."""

    body_a = Body(
        mass=1.0e10,
        position=np.array([-10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=2.0e10,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    state = SimulationState(
        bodies=[body_a, body_b],
    )

    engine = SimulationEngine(
        state=state,
        dt=1.0,
    )

    initial_momentum = (
        body_a.mass * body_a.velocity
        + body_b.mass * body_b.velocity
    )

    engine.step()

    final_momentum = (
        body_a.mass * body_a.velocity
        + body_b.mass * body_b.velocity
    )

    assert np.allclose(
        final_momentum,
        initial_momentum,
        rtol=1e-12,
        atol=1e-12,
    )
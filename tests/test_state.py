import numpy as np

from orbital.physics.body import Body
from orbital.simulation.state import SimulationState


def test_simulation_state_creation():
    """Verifica a criação de um estado de simulação."""

    earth = Body(
        mass=5.972e24,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=6.371e6,
    )

    state = SimulationState(
        bodies=[earth],
        time=0.0,
    )

    assert len(state.bodies) == 1
    assert state.bodies[0] is earth
    assert state.time == 0.0


def test_simulation_state_time():
    """O estado deve armazenar corretamente o tempo da simulação."""

    state = SimulationState(
        bodies=[],
        time=42.5,
    )

    assert state.time == 42.5
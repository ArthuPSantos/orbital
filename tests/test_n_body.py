import numpy as np

from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState
from orbital.physics.body import Body
from orbital.physics.gravity import gravitational_acceleration


def test_three_body_internal_forces_conserve_momentum():
    """As forças internas devem conservar o momento linear total."""

    body_a = Body(
        mass=2.0,
        position=np.array([0.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_b = Body(
        mass=3.0,
        position=np.array([10.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    body_c = Body(
        mass=4.0,
        position=np.array([0.0, 20.0]),
        velocity=np.array([0.0, 0.0]),
        radius=1.0,
    )

    bodies = [body_a, body_b, body_c]

    total_force = np.zeros(2)

    for i, body_a in enumerate(bodies):
        for j, body_b in enumerate(bodies):
            if i == j:
                continue

            acceleration = gravitational_acceleration(
                body_b,
                body_a,
            )

            total_force += body_a.mass * acceleration

    assert np.allclose(
        total_force,
        np.zeros(2),
    )

def test_three_body_simulation_conserves_linear_momentum():
    """Uma simulação de três corpos deve conservar o momento linear."""

    bodies = [
        Body(
            mass=2.0e24,
            position=np.array([-1.0e10, 0.0]),
            velocity=np.array([0.0, 1.0e3]),
            radius=1.0,
        ),
        Body(
            mass=3.0e24,
            position=np.array([1.0e10, 0.0]),
            velocity=np.array([0.0, -500.0]),
            radius=1.0,
        ),
        Body(
            mass=4.0e24,
            position=np.array([0.0, 1.5e10]),
            velocity=np.array([500.0, 0.0]),
            radius=1.0,
        ),
    ]

    state = SimulationState(
        bodies=bodies,
    )

    engine = SimulationEngine(
        state=state,
        dt=1000.0,
    )

    initial_momentum = sum(
        (
            body.mass * body.velocity
            for body in state.bodies
        ),
        start=np.zeros(2),
    )

    for _ in range(100):
        engine.step()

    final_momentum = sum(
        (
            body.mass * body.velocity
            for body in state.bodies
        ),
        start=np.zeros(2),
    )

    assert np.allclose(
        final_momentum,
        initial_momentum,
        rtol=1e-12,
        atol=1e12,
    )



def test_three_body_momentum_and_angular_momentum_are_conserved():
    """
    Verifica a conservação do momento linear e do momento angular
    em um sistema gravitacional isolado de três corpos.

    Como não existem forças externas:

        momento linear total = constante
        momento angular total = constante

    O teste acompanha o sistema durante várias etapas e mede
    o maior erro relativo encontrado.
    """

    import numpy as np

    from orbital.physics.body import Body
    from orbital.physics.gravity import GRAVITATIONAL_CONSTANT
    from orbital.physics.angular_momentum import total_angular_momentum
    from orbital.simulation.engine import SimulationEngine
    from orbital.simulation.state import SimulationState

    bodies = [
        Body(
            mass=2.0e30,
            position=np.array([-1.0e11, 0.0]),
            velocity=np.array([0.0, -500.0]),
            radius=1.0e9,
        ),
        Body(
            mass=6.0e24,
            position=np.array([1.0e11, 0.0]),
            velocity=np.array([0.0, 30000.0]),
            radius=1.0e7,
        ),
        Body(
            mass=1.0e25,
            position=np.array([0.0, 2.0e11]),
            velocity=np.array([-20000.0, 0.0]),
            radius=1.0e7,
        ),
    ]

    state = SimulationState(
        bodies=bodies,
    )

    engine = SimulationEngine(
        state=state,
        dt=3600.0,
    )

    def total_linear_momentum():
        """
        Calcula o momento linear total:

            P = Σ(m_i * v_i)
        """
        return sum(
            (
                body.mass * body.velocity
                for body in state.bodies
            ),
            start=np.zeros(2),
        )

    initial_momentum = total_linear_momentum()
    initial_angular_momentum = total_angular_momentum(
        state.bodies
    )

    maximum_momentum_error = 0.0
    maximum_angular_momentum_error = 0.0

    momentum_scale = np.linalg.norm(initial_momentum)
    angular_momentum_scale = abs(initial_angular_momentum)

    for _ in range(1000):
        engine.step()

        current_momentum = total_linear_momentum()

        current_angular_momentum = total_angular_momentum(
            state.bodies
        )

        momentum_error = np.linalg.norm(
            current_momentum - initial_momentum
        )

        angular_momentum_error = abs(
            current_angular_momentum
            - initial_angular_momentum
        )

        if momentum_scale > 0:
            relative_momentum_error = (
                momentum_error / momentum_scale
            )
            maximum_momentum_error = max(
                maximum_momentum_error,
                relative_momentum_error,
            )

        if angular_momentum_scale > 0:
            relative_angular_momentum_error = (
                angular_momentum_error
                / angular_momentum_scale
            )
            maximum_angular_momentum_error = max(
                maximum_angular_momentum_error,
                relative_angular_momentum_error,
            )

    print(
        f"Erro máximo relativo do momento linear: "
        f"{maximum_momentum_error:.12e}"
    )

    print(
        f"Erro máximo relativo do momento angular: "
        f"{maximum_angular_momentum_error:.12e}"
    )

    assert maximum_momentum_error < 1e-12
    assert maximum_angular_momentum_error < 1e-12



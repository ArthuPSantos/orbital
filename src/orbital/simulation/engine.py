import numpy as np

from orbital.physics.gravity_solver import GravitySolver
from orbital.physics.gravity_solver_protocol import GravitySolverProtocol
from orbital.physics.integrator_protocol import IntegratorProtocol
from orbital.physics.velocity_verlet import VelocityVerlet
from orbital.simulation.state import SimulationState


class SimulationEngine:
    """
    Coordena a evolução temporal de uma simulação.

    O Engine é responsável por:

    - armazenar o estado da simulação;
    - fornecer as acelerações ao integrador;
    - controlar o intervalo de tempo;
    - reutilizar a aceleração calculada no passo anterior.

    A lógica matemática do método de integração permanece
    dentro do integrador.
    """

    def __init__(
        self,
        state: SimulationState,
        dt: float,
        gravity_solver: GravitySolverProtocol | None = None,
        integrator: IntegratorProtocol | None = None,
    ) -> None:
        if not np.isfinite(dt) or dt <= 0:
            raise ValueError(
                "O intervalo dt deve ser um valor finito maior que zero."
            )

        self.state = state
        self.dt = dt

        self.gravity_solver = (
            gravity_solver
            if gravity_solver is not None
            else GravitySolver()
        )

        self.integrator = (
            integrator
            if integrator is not None
            else VelocityVerlet()
        )

        self._accelerations: np.ndarray | None = None

    def _calculate_accelerations(
        self,
        positions: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Calcula as acelerações gravitacionais dos corpos.

        Quando positions não é fornecido, utiliza as posições
        atuais do estado.
        """

        if positions is None:
            positions = np.asarray(
                [body.position for body in self.state.bodies],
                dtype=float,
            )

        masses = np.asarray(
            [body.mass for body in self.state.bodies],
            dtype=float,
        )

        return self.gravity_solver.calculate_accelerations(
            positions,
            masses,
        )

    def _acceleration_function(
        self,
        positions: np.ndarray,
    ) -> np.ndarray:
        """
        Adapta o GravitySolver ao contrato do integrador.

        O integrador trabalha com uma função que recebe posições
        e retorna as acelerações correspondentes.
        """

        return self._calculate_accelerations(
            positions=positions,
        )

    def step(self) -> None:
        """
        Avança a simulação em um intervalo dt.

        A aceleração do passo anterior é reutilizada quando
        disponível. Isso evita recalcular a mesma aceleração
        no início de cada passo.
        """

        bodies = self.state.bodies

        if not bodies:
            self.state.time += self.dt
            return

        positions = np.asarray(
            [body.position for body in bodies],
            dtype=float,
        )

        velocities = np.asarray(
            [body.velocity for body in bodies],
            dtype=float,
        )

        if self._accelerations is None:
            self._accelerations = self._calculate_accelerations(
                positions=positions,
            )

        accelerations = np.asarray(
            self._accelerations,
            dtype=float,
        )

        result = self.integrator.step(
            position=positions,
            velocity=velocities,
            acceleration=accelerations,
            acceleration_function=self._acceleration_function,
            dt=self.dt,
        )

        for body, position, velocity in zip(
            bodies,
            result.position,
            result.velocity,
        ):
            body.position = position
            body.velocity = velocity

        if result.acceleration is None:
            self._accelerations = None
        else:
            self._accelerations = np.asarray(
                result.acceleration,
                dtype=float,
            ).copy()

        self.state.time += self.dt
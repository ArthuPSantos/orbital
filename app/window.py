
import numpy as np
from analysis_panel import AnalysisPanel
from canvas import SimulationCanvas
from experiment_config import ExperimentConfig
from experiment_panel import ExperimentPanel
from guide_panel import GuidePanel
from manual_experiment import run_manual_experiment
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

AU_M = 1.495978707e11
DAY_S = 86_400.0


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "ORBITAL — Computational Laboratory"
        )

        self.resize(1440, 860)

        self._last_simulation_config: (
            ExperimentConfig | None
        ) = None

        self._build_interface()
        self._apply_style()

        self.canvas.animation_finished.connect(
            self._on_animation_finished
        )

    def _build_interface(self) -> None:
        central_widget = QWidget()
        central_widget.setObjectName(
            "central_widget"
        )

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            22,
            18,
            22,
            18,
        )

        main_layout.setSpacing(12)

        header = self._create_header()

        main_layout.addWidget(header)

        self.tabs = QTabWidget()

        self.tabs.setObjectName(
            "main_tabs"
        )

        laboratory_tab = (
            self._create_laboratory_tab()
        )

        analysis_tab = (
            self._create_analysis_tab()
        )

        guide_tab = (
            self._create_guide_tab()
        )

        self.tabs.addTab(
            laboratory_tab,
            "LABORATORY",
        )

        self.tabs.addTab(
            analysis_tab,
            "ANALYSIS",
        )

        self.tabs.addTab(
            guide_tab,
            "GUIDE",
        )

        main_layout.addWidget(
            self.tabs,
            1,
        )

    def _create_header(self) -> QWidget:
        header = QWidget()

        layout = QHBoxLayout(header)

        layout.setContentsMargins(
            2,
            0,
            2,
            0,
        )

        layout.setSpacing(12)

        title_layout = QVBoxLayout()

        title_layout.setSpacing(2)

        brand = QLabel("ORBITAL")
        brand.setObjectName("brand")

        subtitle = QLabel(
            "COMPUTATIONAL GRAVITATIONAL LABORATORY"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        title_layout.addWidget(brand)
        title_layout.addWidget(subtitle)

        layout.addLayout(
            title_layout
        )

        layout.addStretch()

        self.system_status = QLabel(
            "●  SYSTEM READY"
        )

        self.system_status.setObjectName(
            "system_status"
        )

        layout.addWidget(
            self.system_status
        )

        return header

    def _create_laboratory_tab(self) -> QWidget:
        laboratory = QWidget()

        layout = QHBoxLayout(
            laboratory
        )

        layout.setContentsMargins(
            0,
            8,
            0,
            0,
        )

        layout.setSpacing(14)

        self.experiment_panel = (
            ExperimentPanel()
        )

        layout.addWidget(
            self.experiment_panel
        )

        simulation_area = (
            self._create_simulation_area()
        )

        layout.addWidget(
            simulation_area,
            1,
        )

        self.experiment_panel.simulation_speed.currentIndexChanged.connect(
            self._update_animation_speed
        )

        return laboratory

    def _create_analysis_tab(self) -> QWidget:
        self.analysis_panel = AnalysisPanel()

        return self.analysis_panel

    def _create_guide_tab(self) -> QWidget:
        self.guide_panel = GuidePanel()

        return self.guide_panel

    def _create_simulation_area(
        self,
    ) -> QWidget:
        container = QFrame()

        container.setObjectName(
            "simulation_panel"
        )

        layout = QVBoxLayout(container)

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setSpacing(10)

        self.canvas = SimulationCanvas()

        layout.addWidget(
            self.canvas,
            1,
        )

        controls = (
            self._create_simulation_controls()
        )

        layout.addWidget(
            controls
        )

        metrics = self._create_metrics()

        layout.addWidget(
            metrics
        )

        return container

    def _create_simulation_controls(
        self,
    ) -> QWidget:
        controls = QWidget()

        layout = QHBoxLayout(controls)

        layout.setContentsMargins(
            4,
            0,
            4,
            0,
        )

        layout.setSpacing(8)

        self.play_button = QPushButton(
            "▶  PLAY"
        )

        self.play_button.setObjectName(
            "run_button"
        )

        self.play_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.play_button.clicked.connect(
            self._toggle_animation
        )

        self.reset_button = QPushButton(
            "↺  RESET"
        )

        self.reset_button.setObjectName(
            "run_button"
        )

        self.reset_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.reset_button.clicked.connect(
            self._reset_animation
        )

        layout.addWidget(
            self.play_button
        )

        layout.addWidget(
            self.reset_button
        )

        layout.addStretch()

        return controls

    def _create_metrics(self) -> QWidget:
        metrics = QFrame()

        metrics.setObjectName(
            "metrics"
        )

        layout = QHBoxLayout(metrics)

        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(24)

        self.energy_value = (
            self._create_metric(
                layout,
                "ENERGY ERROR",
            )
        )

        self.angular_momentum_value = (
            self._create_metric(
                layout,
                "ANGULAR MOMENTUM",
            )
        )

        self.computation_time_value = (
            self._create_metric(
                layout,
                "COMPUTATION TIME",
            )
        )

        self.steps_value = (
            self._create_metric(
                layout,
                "STEPS",
            )
        )

        return metrics

    def _create_metric(
        self,
        layout: QHBoxLayout,
        title: str,
    ) -> QLabel:
        container = QWidget()

        container_layout = QVBoxLayout(
            container
        )

        container_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        container_layout.setSpacing(3)

        title_label = QLabel(title)

        title_label.setObjectName(
            "metric_title"
        )

        value_label = QLabel("—")

        value_label.setObjectName(
            "metric_value"
        )

        container_layout.addWidget(
            title_label
        )

        container_layout.addWidget(
            value_label
        )

        layout.addWidget(
            container
        )

        return value_label

    def _toggle_animation(self) -> None:
        current_config = (
            self.experiment_panel.get_config()
        )

        if self._last_simulation_config is None:
            self._run_experiment(
                current_config
            )
            return

        if (
            current_config
            != self._last_simulation_config
        ):
            self._run_experiment(
                current_config
            )
            return

        running = (
            self.canvas.toggle_animation()
        )

        if running:
            self.play_button.setText(
                "❚❚  PAUSE"
            )

            self.system_status.setText(
                "●  SIMULATION RUNNING"
            )

        else:
            self.play_button.setText(
                "▶  PLAY"
            )

            self.system_status.setText(
                "●  SIMULATION PAUSED"
            )

    def _reset_animation(self) -> None:
        if self._last_simulation_config is None:
            return

        self.canvas.reset_animation()

        self.play_button.setText(
            "▶  PLAY"
        )

        self.system_status.setText(
            "●  SYSTEM READY"
        )

    def _update_animation_speed(
        self,
    ) -> None:
        speed = (
            self.experiment_panel
            .get_simulation_speed()
        )

        self.canvas.set_animation_speed(
            speed
        )

    def _on_animation_finished(self) -> None:
        self.play_button.setText(
            "▶  PLAY"
        )

        self.system_status.setText(
            "●  SIMULATION COMPLETE"
        )

    def _run_experiment(
        self,
        config: ExperimentConfig | None = None,
    ) -> None:
        self.system_status.setText(
            "●  RUNNING SIMULATION"
        )

        self.play_button.setText(
            "❚❚  PAUSE"
        )

        QApplication.processEvents()

        if config is None:
            config = (
                self.experiment_panel
                .get_config()
            )

        print()
        print(
            "ORBITAL — RUNNING EXPERIMENT"
        )
        print("-" * 32)

        print(
            f"Primary mass: "
            f"{config.star_mass_kg:.6e} kg"
        )

        print(
            f"Secondary mass: "
            f"{config.planet_mass_kg:.6e} kg"
        )

        print(
            f"Distance: "
            f"{config.distance_m:.6e} m"
        )

        print(
            f"Velocity: "
            f"{config.velocity_m_per_s:.6e} m/s"
        )

        print(
            f"Duration: "
            f"{config.duration_s:.6e} s"
        )

        print(
            f"Precision: "
            f"{config.precision}"
        )

        print("-" * 32)

        try:
            results = run_manual_experiment(
                config
            )

        except (ValueError, ArithmeticError, RuntimeError, TypeError) as error:
            self.system_status.setText(
                "●  SIMULATION ERROR"
            )

            self.play_button.setText(
                "▶  PLAY"
            )

            print(
                f"ERROR: {error}"
            )

            return

        self.canvas.set_trajectory(
            results["trajectory_planet"],
            results["trajectory_star"],
            config.star_mass_kg,
            config.planet_mass_kg,
            results["trajectory_velocity"],
            results["trajectory_times"],
        )

        speed = (
            self.experiment_panel
            .get_simulation_speed()
        )

        self.canvas.set_animation_speed(
            speed
        )

        self.canvas.start_animation()

        self._last_simulation_config = config

        self._update_simulation_information(
            results["engine"]
        )

        self._update_metrics(
            results
        )

        self.analysis_panel.set_results(
            results
        )

        print(
            f"Steps: {results['steps']}"
        )

        print(
            "Energy error: "
            f"{results['energy_error']:.6e}"
        )

        print(
            "Angular momentum error: "
            f"{results['angular_momentum_error']:.6e}"
        )

        print(
            "Computation time: "
            f"{results['computation_time']:.4f} s"
        )

        print("-" * 32)
        print("Simulation complete.")
        print()

        self.system_status.setText(
            "●  SIMULATION RUNNING"
        )

    def _update_simulation_information(
        self,
        engine,
    ) -> None:
        if not engine.state.bodies:
            return

        if len(engine.state.bodies) < 2:
            return

        planet = (
            engine.state.bodies[1]
        )

        distance_au = (
            np.linalg.norm(
                planet.position
            )
            / AU_M
        )

        velocity_km_s = (
            np.linalg.norm(
                planet.velocity
            )
            / 1_000.0
        )

        time_days = (
            engine.state.time
            / DAY_S
        )

        self.canvas.set_simulation_info(
            time_days,
            distance_au,
            velocity_km_s,
        )

    def _update_metrics(
        self,
        results: dict,
    ) -> None:
        self.energy_value.setText(
            f"{results['energy_error']:.3e}"
        )

        self.angular_momentum_value.setText(
            f"{results['angular_momentum_error']:.3e}"
        )

        self.computation_time_value.setText(
            f"{results['computation_time']:.4f} s"
        )

        self.steps_value.setText(
            f"{results['steps']:,}"
        )

    def _apply_style(self) -> None:
        from styles import get_stylesheet

        self.setStyleSheet(
            get_stylesheet()
        )

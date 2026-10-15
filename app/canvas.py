import numpy as np
from PySide6.QtCore import (
    QPointF,
    QRectF,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget

AU_M = 1.495978707e11


class SimulationCanvas(QWidget):
    animation_finished = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("simulation_canvas")
        self.setMinimumSize(500, 400)

        self._trajectory_planet: np.ndarray | None = None
        self._trajectory_star: np.ndarray | None = None
        self._trajectory_velocity: np.ndarray | None = None
        self._trajectory_times: np.ndarray | None = None

        self._star_mass = 1.989e30
        self._planet_mass = 5.972e24

        self._planet_position = np.array(
            [AU_M, 0.0],
            dtype=float,
        )

        self._star_position = np.array(
            [0.0, 0.0],
            dtype=float,
        )

        self._simulation_time_days = 0.0
        self._planet_distance_au = 1.0
        self._planet_velocity_km_s = 29.78

        self._animation_index = 0
        self._animation_speed = 4

        self._animation_timer = QTimer(self)

        self._animation_timer.setInterval(30)
        self._animation_timer.timeout.connect(
            self._advance_animation
        )

        self._animation_running = False

    def set_trajectory(
        self,
        trajectory_planet: np.ndarray,
        trajectory_star: np.ndarray,
        star_mass: float,
        planet_mass: float,
        trajectory_velocity: np.ndarray | None = None,
        trajectory_times: np.ndarray | None = None,
    ) -> None:
        self._animation_timer.stop()

        self._animation_running = False
        self._animation_index = 0

        self._trajectory_planet = np.asarray(
            trajectory_planet,
            dtype=float,
        )

        self._trajectory_star = np.asarray(
            trajectory_star,
            dtype=float,
        )

        if trajectory_velocity is not None:
            self._trajectory_velocity = np.asarray(
                trajectory_velocity,
                dtype=float,
            )
        else:
            self._trajectory_velocity = None

        if trajectory_times is not None:
            self._trajectory_times = np.asarray(
                trajectory_times,
                dtype=float,
            )
        else:
            self._trajectory_times = None

        self._star_mass = star_mass
        self._planet_mass = planet_mass

        if len(self._trajectory_planet) > 0:
            self._planet_position = (
                self._trajectory_planet[0].copy()
            )

        if len(self._trajectory_star) > 0:
            self._star_position = (
                self._trajectory_star[0].copy()
            )

        self._update_animation_information()

        self.update()

    def set_simulation_info(
        self,
        time_days: float,
        distance_au: float,
        velocity_km_s: float,
    ) -> None:
        self._simulation_time_days = time_days
        self._planet_distance_au = distance_au
        self._planet_velocity_km_s = velocity_km_s

        self.update()

    def set_animation_speed(
        self,
        speed: int,
    ) -> None:
        speed = max(speed, 1)

        self._animation_speed = speed

    def start_animation(self) -> None:
        if (
            self._trajectory_planet is None
            or len(self._trajectory_planet) == 0
        ):
            return

        self._animation_index = 0
        self._animation_running = True

        self._update_animation_position()

        self._animation_timer.start()

    def stop_animation(self) -> None:
        self._animation_timer.stop()
        self._animation_running = False

    def toggle_animation(self) -> bool:
        if self._trajectory_planet is None:
            return False

        if len(self._trajectory_planet) == 0:
            return False

        if self._animation_running:
            self.stop_animation()
            return False

        if (
            self._animation_index
            >= len(self._trajectory_planet) - 1
        ):
            self._animation_index = 0

        self._animation_running = True

        self._update_animation_position()

        self._animation_timer.start()

        return True

    def reset_animation(self) -> None:
        if self._trajectory_planet is None:
            return

        if len(self._trajectory_planet) == 0:
            return

        self._animation_timer.stop()

        self._animation_running = False
        self._animation_index = 0

        self._update_animation_position()

    def is_animation_running(self) -> bool:
        return self._animation_running

    def _advance_animation(self) -> None:
        if self._trajectory_planet is None:
            self.stop_animation()
            return

        self._animation_index += self._animation_speed

        if (
            self._animation_index
            >= len(self._trajectory_planet)
        ):
            self._animation_index = (
                len(self._trajectory_planet) - 1
            )

            self._update_animation_position()
            self.stop_animation()

            self.animation_finished.emit()

            return

        self._update_animation_position()

    def _update_animation_position(self) -> None:
        if self._trajectory_planet is None:
            return

        if self._trajectory_star is None:
            return

        index = self._animation_index

        self._planet_position = (
            self._trajectory_planet[index].copy()
        )

        self._star_position = (
            self._trajectory_star[index].copy()
        )

        if self._trajectory_velocity is not None:
            velocity = (
                self._trajectory_velocity[index]
            )

            self._planet_velocity_km_s = (
                np.linalg.norm(velocity)
                / 1_000.0
            )

        if self._trajectory_times is not None:
            self._simulation_time_days = (
                self._trajectory_times[index]
                / 86_400.0
            )

        self._planet_distance_au = (
            np.linalg.norm(
                self._planet_position
            )
            / AU_M
        )

        self.update()

    def _update_animation_information(self) -> None:
        if self._trajectory_planet is None:
            return

        if len(self._trajectory_planet) == 0:
            return

        index = min(
            self._animation_index,
            len(self._trajectory_planet) - 1,
        )

        self._planet_position = (
            self._trajectory_planet[index].copy()
        )

        if self._trajectory_star is not None:
            self._star_position = (
                self._trajectory_star[index].copy()
            )

        if self._trajectory_velocity is not None:
            velocity = (
                self._trajectory_velocity[index]
            )

            self._planet_velocity_km_s = (
                np.linalg.norm(velocity)
                / 1_000.0
            )

        if self._trajectory_times is not None:
            self._simulation_time_days = (
                self._trajectory_times[index]
                / 86_400.0
            )

        self._planet_distance_au = (
            np.linalg.norm(
                self._planet_position
            )
            / AU_M
        )

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        self._draw_background(painter)
        self._draw_stars(painter)

        if self._trajectory_planet is not None:
            self._draw_real_trajectory(painter)
        else:
            self._draw_default_orbit(painter)

        self._draw_bodies(painter)
        self._draw_information(painter)
        self._draw_legend(painter)

        if self._trajectory_planet is not None:
            self._draw_center_of_mass(
                painter
            )

        painter.end()

    def _draw_background(
        self,
        painter: QPainter,
    ) -> None:
        gradient = QLinearGradient(
            0,
            0,
            0,
            self.height(),
        )

        gradient.setColorAt(
            0.0,
            QColor("#05080b"),
        )

        gradient.setColorAt(
            1.0,
            QColor("#020407"),
        )

        painter.fillRect(
            self.rect(),
            gradient,
        )

    def _draw_stars(
        self,
        painter: QPainter,
    ) -> None:
        rng = np.random.default_rng(42)

        width = self.width()
        height = self.height()

        painter.save()

        for _ in range(180):
            x = rng.uniform(0, width)
            y = rng.uniform(0, height)

            radius = rng.uniform(0.3, 1.1)

            alpha = int(
                rng.uniform(35, 120)
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor(
                    190,
                    205,
                    220,
                    alpha,
                )
            )

            painter.drawEllipse(
                QPointF(x, y),
                radius,
                radius,
            )

        painter.restore()

    def _draw_real_trajectory(
        self,
        painter: QPainter,
    ) -> None:
        if self._trajectory_planet is None:
            return

        if len(self._trajectory_planet) < 2:
            return

        center, scale = (
            self._calculate_view_transform()
        )

        painter.save()

        visible_points = self._trajectory_planet[
            : self._animation_index + 1
        ]

        if len(visible_points) < 2:
            painter.restore()
            return

        points = []

        for position in visible_points:
            points.append(
                self._world_to_screen(
                    position,
                    center,
                    scale,
                )
            )

        for index in range(
            len(points) - 1
        ):
            start = points[index]
            end = points[index + 1]

            alpha = int(
                35
                + 80
                * index
                / max(
                    1,
                    len(points) - 1,
                )
            )

            painter.setPen(
                QColor(
                    110,
                    145,
                    175,
                    alpha,
                )
            )

            painter.drawLine(
                start,
                end,
            )

        painter.restore()

    def _draw_default_orbit(
        self,
        painter: QPainter,
    ) -> None:
        center_x = self.width() / 2
        center_y = self.height() / 2

        orbit_width = min(
            self.width(),
            self.height(),
        ) * 0.62

        orbit_height = orbit_width * 0.62

        painter.save()

        painter.setPen(
            QColor(
                75,
                100,
                120,
                80,
            )
        )

        painter.drawEllipse(
            QRectF(
                center_x - orbit_width / 2,
                center_y - orbit_height / 2,
                orbit_width,
                orbit_height,
            )
        )

        painter.restore()

    def _draw_bodies(
        self,
        painter: QPainter,
    ) -> None:
        if self._trajectory_planet is not None:
            center, scale = (
                self._calculate_view_transform()
            )

            star_screen = self._world_to_screen(
                self._star_position,
                center,
                scale,
            )

            planet_screen = self._world_to_screen(
                self._planet_position,
                center,
                scale,
            )

            self._draw_star(
                painter,
                star_screen,
            )

            self._draw_planet(
                painter,
                planet_screen,
            )

            return

        center_x = self.width() / 2
        center_y = self.height() / 2

        star_position = QPointF(
            center_x,
            center_y,
        )

        planet_position = QPointF(
            center_x + 180,
            center_y,
        )

        self._draw_star(
            painter,
            star_position,
        )

        self._draw_planet(
            painter,
            planet_position,
        )

    def _draw_information(
        self,
        painter: QPainter,
    ) -> None:
        painter.save()

        title_font = QFont("Segoe UI")
        title_font.setPixelSize(8)
        title_font.setWeight(
            QFont.Weight.DemiBold
        )

        value_font = QFont("Consolas")
        value_font.setPixelSize(11)

        x = 18
        y = 20

        information = [
            (
                "TIME",
                f"{self._simulation_time_days:.2f} DAYS",
            ),
            (
                "DISTANCE",
                f"{self._planet_distance_au:.3f} AU",
            ),
            (
                "VELOCITY",
                f"{self._planet_velocity_km_s:.3f} KM/S",
            ),
        ]

        for title, value in information:
            painter.setFont(title_font)
            painter.setPen(
                QColor("#66737f")
            )

            painter.drawText(
                x,
                y,
                title,
            )

            y += 14

            painter.setFont(value_font)
            painter.setPen(
                QColor("#dce4ea")
            )

            painter.drawText(
                x,
                y,
                value,
            )

            y += 28

        painter.restore()

    def _draw_legend(
        self,
        painter: QPainter,
    ) -> None:
        painter.save()

        title_font = QFont("Segoe UI")
        title_font.setPixelSize(8)
        title_font.setWeight(
            QFont.Weight.DemiBold
        )

        item_font = QFont("Segoe UI")
        item_font.setPixelSize(9)

        x = 18
        y = self.height() - 62

        painter.setFont(title_font)
        painter.setPen(
            QColor("#66737f")
        )

        painter.drawText(
            x,
            y,
            "SYSTEM OBJECTS",
        )

        y += 17

        items = [
            (
                "PRIMARY BODY",
                QColor("#e2b35c"),
            ),
            (
                "SECONDARY BODY",
                QColor("#6f9eb5"),
            ),
            (
                "CENTER OF MASS",
                QColor("#9aa8b3"),
            ),
        ]

        for name, color in items:
            painter.setPen(
                color
            )

            painter.setFont(
                item_font
            )

            painter.drawText(
                x,
                y,
                name,
            )

            y += 14

        painter.restore()

    def _draw_center_of_mass(
        self,
        painter: QPainter,
    ) -> None:
        if (
            self._trajectory_planet is None
            or self._trajectory_star is None
        ):
            return

        center, scale = (
            self._calculate_view_transform()
        )

        star = self._star_position
        planet = self._planet_position

        total_mass = (
            self._star_mass
            + self._planet_mass
        )

        if total_mass <= 0.0:
            return

        center_of_mass = (
            self._star_mass * star
            + self._planet_mass * planet
        ) / total_mass

        screen_position = self._world_to_screen(
            center_of_mass,
            center,
            scale,
        )

        painter.save()

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        glow = QRadialGradient(
            screen_position,
            18,
        )

        glow.setColorAt(
            0.0,
            QColor(
                230,
                235,
                240,
                90,
            ),
        )

        glow.setColorAt(
            0.45,
            QColor(
                190,
                205,
                215,
                45,
            ),
        )

        glow.setColorAt(
            1.0,
            QColor(
                160,
                175,
                185,
                0,
            ),
        )

        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            screen_position,
            18,
            18,
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.setPen(
            QColor(
                220,
                230,
                238,
                210,
            )
        )

        painter.drawEllipse(
            screen_position,
            7,
            7,
        )

        painter.setBrush(
            QColor(
                235,
                240,
                245,
                230,
            )
        )

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            screen_position,
            2.5,
            2.5,
        )

        painter.setPen(
            QColor(
                205,
                218,
                228,
                190,
            )
        )

        painter.drawLine(
            QPointF(
                screen_position.x() - 11,
                screen_position.y(),
            ),
            QPointF(
                screen_position.x() + 11,
                screen_position.y(),
            ),
        )

        painter.drawLine(
            QPointF(
                screen_position.x(),
                screen_position.y() - 11,
            ),
            QPointF(
                screen_position.x(),
                screen_position.y() + 11,
            ),
        )

        font = QFont("Segoe UI")
        font.setPixelSize(9)
        font.setWeight(
            QFont.Weight.DemiBold
        )

        painter.setFont(font)

        painter.setPen(
            QColor(
                190,
                205,
                215,
                210,
            )
        )

        painter.drawText(
            QPointF(
                screen_position.x() + 14,
                screen_position.y() - 10,
            ),
            "CENTER OF MASS",
        )

        painter.restore()

    def _draw_star(
        self,
        painter: QPainter,
        position: QPointF,
    ) -> None:
        painter.save()

        glow = QRadialGradient(
            position,
            85,
        )

        glow.setColorAt(
            0.0,
            QColor(
                255,
                215,
                130,
                80,
            ),
        )

        glow.setColorAt(
            0.45,
            QColor(
                245,
                180,
                75,
                35,
            ),
        )

        glow.setColorAt(
            1.0,
            QColor(
                255,
                170,
                60,
                0,
            ),
        )

        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            position,
            85,
            85,
        )

        surface = QRadialGradient(
            QPointF(
                position.x() - 7,
                position.y() - 9,
            ),
            30,
        )

        surface.setColorAt(
            0.0,
            QColor("#fff3c4"),
        )

        surface.setColorAt(
            0.45,
            QColor("#ffd36b"),
        )

        surface.setColorAt(
            1.0,
            QColor("#d87925"),
        )

        painter.setBrush(surface)

        painter.drawEllipse(
            position,
            30,
            30,
        )

        painter.restore()

    def _draw_planet(
        self,
        painter: QPainter,
        position: QPointF,
    ) -> None:
        painter.save()

        atmosphere = QRadialGradient(
            position,
            15,
        )

        atmosphere.setColorAt(
            0.0,
            QColor(
                90,
                150,
                190,
                45,
            ),
        )

        atmosphere.setColorAt(
            0.75,
            QColor(
                70,
                120,
                165,
                25,
            ),
        )

        atmosphere.setColorAt(
            1.0,
            QColor(
                50,
                100,
                150,
                0,
            ),
        )

        painter.setBrush(atmosphere)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            position,
            15,
            15,
        )

        surface = QRadialGradient(
            QPointF(
                position.x() - 2,
                position.y() - 3,
            ),
            8,
        )

        surface.setColorAt(
            0.0,
            QColor("#8bb8d0"),
        )

        surface.setColorAt(
            0.65,
            QColor("#47758e"),
        )

        surface.setColorAt(
            1.0,
            QColor("#203846"),
        )

        painter.setBrush(surface)

        painter.drawEllipse(
            position,
            8,
            8,
        )

        painter.restore()

    def _calculate_view_transform(
        self,
    ) -> tuple[np.ndarray, float]:
        positions = []

        if self._trajectory_planet is not None:
            positions.append(
                self._trajectory_planet
            )

        if self._trajectory_star is not None:
            positions.append(
                self._trajectory_star
            )

        if not positions:
            return (
                np.array(
                    [0.0, 0.0],
                    dtype=float,
                ),
                1.0,
            )

        all_positions = np.vstack(
            positions
        )

        minimum = all_positions.min(
            axis=0
        )

        maximum = all_positions.max(
            axis=0
        )

        center = (
            minimum + maximum
        ) / 2.0

        span = np.max(
            maximum - minimum
        )

        if span <= 0.0:
            span = AU_M

        margin = 0.82

        scale = (
            min(
                self.width(),
                self.height(),
            )
            * margin
            / span
        )

        return center, scale

    def _world_to_screen(
        self,
        position: np.ndarray,
        center: np.ndarray,
        scale: float,
    ) -> QPointF:
        screen_center_x = self.width() / 2
        screen_center_y = self.height() / 2

        x = (
            screen_center_x
            + (
                position[0]
                - center[0]
            )
            * scale
        )

        y = (
            screen_center_y
            - (
                position[1]
                - center[1]
            )
            * scale
        )

        return QPointF(
            x,
            y,
        )
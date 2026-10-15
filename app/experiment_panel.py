
from experiment_config import ExperimentConfig
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class NoWheelSpinBox(QDoubleSpinBox):
    def wheelEvent(self, event) -> None:
        event.ignore()


class NoWheelComboBox(QComboBox):
    def wheelEvent(self, event) -> None:
        event.ignore()


class ExperimentPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("panel")
        self._build_interface()

    def _build_interface(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("experiment_content")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)

        section = QLabel("EXPERIMENT")
        section.setObjectName("section_title")

        description = QLabel("Configure the physical system")
        description.setObjectName("description")

        layout.addWidget(section)
        layout.addWidget(description)

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)

        system_title = QLabel("SYSTEM")
        system_title.setObjectName("field_title")
        layout.addWidget(system_title)

        primary_body = self._create_body_card(
            "PRIMARY BODY",
            "Sun",
        )
        secondary_body = self._create_body_card(
            "SECONDARY BODY",
            "Earth",
        )

        layout.addWidget(primary_body)
        layout.addWidget(secondary_body)

        primary_mass_title = QLabel("PRIMARY MASS")
        primary_mass_title.setObjectName("field_title")
        layout.addWidget(primary_mass_title)

        primary_mass_layout = QHBoxLayout()
        primary_mass_layout.setSpacing(6)

        self.star_mass = self._create_spinbox(
            1.0,
            0.000001,
            1000.0,
            2,
        )
        self.star_mass_unit = self._create_combo(
            ["SOLAR MASSES", "KG"],
            0,
        )

        primary_mass_layout.addWidget(self.star_mass, 1)
        primary_mass_layout.addWidget(self.star_mass_unit, 1)
        layout.addLayout(primary_mass_layout)

        secondary_mass_title = QLabel("SECONDARY MASS")
        secondary_mass_title.setObjectName("field_title")
        layout.addWidget(secondary_mass_title)

        secondary_mass_layout = QHBoxLayout()
        secondary_mass_layout.setSpacing(6)

        self.planet_mass = self._create_spinbox(
            1.0,
            0.000001,
            1000000.0,
            2,
        )
        self.planet_mass_unit = self._create_combo(
            ["EARTH MASSES", "SOLAR MASSES", "KG"],
            0,
        )

        secondary_mass_layout.addWidget(self.planet_mass, 1)
        secondary_mass_layout.addWidget(
            self.planet_mass_unit,
            1,
        )
        layout.addLayout(secondary_mass_layout)

        distance_title = QLabel("DISTANCE")
        distance_title.setObjectName("field_title")
        layout.addWidget(distance_title)

        distance_layout = QHBoxLayout()
        distance_layout.setSpacing(6)

        self.distance = self._create_spinbox(
            1.0,
            0.000001,
            1000000.0,
            3,
        )
        self.distance_unit = self._create_combo(
            ["AU", "KM", "M"],
            0,
        )

        distance_layout.addWidget(self.distance, 1)
        distance_layout.addWidget(self.distance_unit, 1)
        layout.addLayout(distance_layout)

        velocity_title = QLabel("VELOCITY")
        velocity_title.setObjectName("field_title")
        layout.addWidget(velocity_title)

        velocity_layout = QHBoxLayout()
        velocity_layout.setSpacing(6)

        self.velocity = self._create_spinbox(
            29.78,
            0.0,
            1000000.0,
            3,
        )
        self.velocity_unit = self._create_combo(
            ["KM/S", "M/S"],
            0,
        )

        velocity_layout.addWidget(self.velocity, 1)
        velocity_layout.addWidget(self.velocity_unit, 1)
        layout.addLayout(velocity_layout)

        duration_title = QLabel("DURATION")
        duration_title.setObjectName("field_title")
        layout.addWidget(duration_title)

        duration_layout = QHBoxLayout()
        duration_layout.setSpacing(6)

        self.duration = self._create_spinbox(
            1.0,
            0.000001,
            100000.0,
            3,
        )
        self.duration_unit = self._create_combo(
            ["YEAR", "MONTH", "DAY", "HOUR"],
            0,
        )

        duration_layout.addWidget(self.duration, 1)
        duration_layout.addWidget(self.duration_unit, 1)
        layout.addLayout(duration_layout)

        precision_title = QLabel("PRECISION")
        precision_title.setObjectName("field_title")
        layout.addWidget(precision_title)

        self.precision = self._create_combo(
            ["FAST", "BALANCED", "HIGH", "CUSTOM"],
            1,
        )
        layout.addWidget(self.precision)

        speed_title = QLabel("SIMULATION SPEED")
        speed_title.setObjectName("field_title")
        layout.addWidget(speed_title)

        self.simulation_speed = self._create_combo(
            ["1× REAL TIME", "2×", "4×", "8×", "16×", "32×"],
            2,
        )
        layout.addWidget(self.simulation_speed)

        layout.addStretch()

        scroll_area.setWidget(content)
        outer_layout.addWidget(scroll_area)

    def get_config(self) -> ExperimentConfig:
        return ExperimentConfig(
            star_mass=self.star_mass.value(),
            star_mass_unit=self.star_mass_unit.currentText(),
            planet_mass=self.planet_mass.value(),
            planet_mass_unit=self.planet_mass_unit.currentText(),
            distance=self.distance.value(),
            distance_unit=self.distance_unit.currentText(),
            velocity=self.velocity.value(),
            velocity_unit=self.velocity_unit.currentText(),
            duration=self.duration.value(),
            duration_unit=self.duration_unit.currentText(),
            precision=self.precision.currentText(),
        )

    def get_simulation_speed(self) -> int:
        speed_text = self.simulation_speed.currentText()

        if speed_text == "1× REAL TIME":
            return 1

        return int(speed_text.replace("×", ""))

    def _create_spinbox(
        self,
        value: float,
        minimum: float,
        maximum: float,
        decimals: int,
    ) -> QDoubleSpinBox:
        spinbox = NoWheelSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)
        spinbox.setDecimals(decimals)
        spinbox.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )
        return spinbox

    def _create_combo(
        self,
        items: list[str],
        current_index: int,
    ) -> QComboBox:
        combo = NoWheelComboBox()
        combo.addItems(items)
        combo.setCurrentIndex(current_index)
        return combo

    def _create_body_card(
        self,
        category: str,
        name: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("body_card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)

        category_label = QLabel(category)
        category_label.setObjectName("body_card_category")

        name_label = QLabel(name)
        name_label.setObjectName("body_card_name")

        layout.addWidget(category_label)
        layout.addWidget(name_label)

        return card

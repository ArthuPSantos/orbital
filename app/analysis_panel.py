"""Aba ANALYSIS do ORBITAL.

Dois painéis verticais:

    TRAJECTORY      órbita em X/Y
    PHYSICAL STATE  seletor de grandeza + gráfico em função do tempo

As margens dos gráficos são calculadas em pontos e ajustadas conforme o
redimensionamento. Os painéis expandem junto com a janela, sem impor a largura
fixa da barra lateral do laboratório.
"""

from __future__ import annotations

from typing import Any, NamedTuple

import matplotlib

matplotlib.use("QtAgg")

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

AU_M = 1.495978707e11
DAY_S = 86_400.0

BACKGROUND = "#0c1117"
TEXT = "#7f8c98"
TICK = "#687582"
SPINE = "#26313b"
CARD_BORDER = "#1b252e"
GRID = "#7f8c98"
STAR_COLOR = "#d6a550"
PLANET_COLOR = "#5fa8d3"
STATE_COLOR = "#5fa8d3"

FONT_SIZE = 8

_DEBUG_LAYOUT = False
_BUILD = "analysis_panel build 5"

_CARD_STYLE = (
    "QFrame#analysis_card {"
    f" background-color: {BACKGROUND};"
    f" border: 1px solid {CARD_BORDER};"
    " border-radius: 6px;"
    " }"
)

_PANEL_TITLE_STYLE = "font-size: 10px;"


class _Margins(NamedTuple):
    """Espaço reservado fora dos eixos, em pontos."""

    left: float
    right: float
    top: float
    bottom: float


_TRAJECTORY_MARGINS = _Margins(left=44.0, right=12.0, top=22.0, bottom=25.0)
_STATE_MARGINS = _Margins(left=40.0, right=12.0, top=13.0, bottom=25.0)
_PLACEHOLDER_MARGINS = _Margins(left=6.0, right=6.0, top=6.0, bottom=6.0)

_STATE_SERIES: tuple[tuple[str, str, float, str], ...] = (
    ("DISTANCE", "distance_history", 1.0 / AU_M, "DISTANCE [AU]"),
    ("VELOCITY", "velocity_history", 1.0 / 1_000.0, "VELOCITY [KM/S]"),
    ("ENERGY", "energy_history", 1.0, "TOTAL ENERGY [J]"),
    (
        "ANGULAR MOMENTUM",
        "angular_momentum_history",
        1.0,
        "ANGULAR MOMENTUM [KG·M²/S]",
    ),
)


def _format_ylabel(label: str) -> str:
    """Quebra rótulos longos em nome e unidade."""

    if len(label) > 20 and " [" in label:
        name, unit = label.split(" [", 1)
        return f"{name}\n[{unit}"

    return label


def _apply_margins(figure: Figure, margins: _Margins) -> None:
    """Converte margens em pontos para frações da figura atual."""

    width = figure.get_figwidth() * 72.0
    height = figure.get_figheight() * 72.0

    if (
        width <= margins.left + margins.right + 40.0
        or height <= margins.top + margins.bottom + 40.0
    ):
        return

    figure.subplots_adjust(
        left=margins.left / width,
        right=1.0 - margins.right / width,
        top=1.0 - margins.top / height,
        bottom=margins.bottom / height,
    )

    _fit_ylabel(figure)


def _fit_ylabel(figure: Figure) -> None:
    """Reduz a fonte do rótulo Y quando não há altura suficiente."""

    if not figure.axes:
        return

    axis = figure.axes[0]
    label = axis.yaxis.label

    if not label.get_text():
        return

    try:
        renderer = figure.canvas.get_renderer()
    except AttributeError:
        return

    label.set_fontsize(FONT_SIZE)

    available = axis.get_window_extent(renderer).height
    needed = label.get_window_extent(renderer).height

    if needed > available > 0:
        label.set_fontsize(max(5.0, FONT_SIZE * available / needed * 0.97))


def _style_axis(axis: Any) -> None:
    axis.set_facecolor(BACKGROUND)
    axis.set_axisbelow(True)

    axis.tick_params(
        colors=TICK,
        labelsize=FONT_SIZE,
        length=2.5,
        width=0.6,
        pad=2.0,
    )

    axis.xaxis.label.set_color(TEXT)
    axis.yaxis.label.set_color(TEXT)

    for offset in (
        axis.xaxis.get_offset_text(),
        axis.yaxis.get_offset_text(),
    ):
        offset.set_color(TICK)
        offset.set_fontsize(FONT_SIZE)

    axis.grid(
        True,
        color=GRID,
        linewidth=0.5,
        alpha=0.14,
    )

    for spine in axis.spines.values():
        spine.set_color(SPINE)
        spine.set_linewidth(0.8)


def _plot_placeholder(figure: Figure, message: str) -> _Margins:
    figure.clear()
    figure.patch.set_facecolor(BACKGROUND)

    axis = figure.add_subplot(111)
    axis.set_facecolor(BACKGROUND)

    axis.text(
        0.5,
        0.5,
        message,
        transform=axis.transAxes,
        ha="center",
        va="center",
        color=TICK,
        fontsize=10,
    )

    axis.set_xticks([])
    axis.set_yticks([])

    for spine in axis.spines.values():
        spine.set_visible(False)

    return _PLACEHOLDER_MARGINS


def _plot_trajectory(
    figure: Figure,
    results: dict[str, Any] | None,
) -> _Margins:
    """Desenha a trajetória X/Y."""

    if results is None:
        return _plot_placeholder(
            figure,
            "Run a simulation to display the trajectory.",
        )

    star = np.asarray(results["trajectory_star"], dtype=float) / AU_M
    planet = np.asarray(results["trajectory_planet"], dtype=float) / AU_M

    if (
        star.ndim != 2
        or planet.ndim != 2
        or star.shape[0] == 0
        or planet.shape[0] == 0
        or star.shape[1] < 2
        or planet.shape[1] < 2
    ):
        return _plot_placeholder(figure, "No trajectory data.")

    figure.clear()
    figure.patch.set_facecolor(BACKGROUND)

    axis = figure.add_subplot(111)
    _style_axis(axis)

    (star_line,) = axis.plot(
        star[:, 0],
        star[:, 1],
        color=STAR_COLOR,
        linewidth=1.2,
        label="STAR TRAJECTORY",
    )

    (planet_line,) = axis.plot(
        planet[:, 0],
        planet[:, 1],
        color=PLANET_COLOR,
        linewidth=1.4,
        label="PLANET TRAJECTORY",
    )

    axis.scatter(
        star[-1, 0],
        star[-1, 1],
        s=36,
        color=star_line.get_color(),
        edgecolors=BACKGROUND,
        linewidths=0.8,
        zorder=5,
    )

    axis.scatter(
        planet[-1, 0],
        planet[-1, 1],
        s=26,
        color=planet_line.get_color(),
        edgecolors=BACKGROUND,
        linewidths=0.8,
        zorder=5,
    )

    axis.set_xlabel("X [AU]", fontsize=FONT_SIZE, labelpad=2.0)
    axis.set_ylabel("Y [AU]", fontsize=FONT_SIZE, labelpad=2.0)

    legend = axis.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        borderaxespad=0.3,
        ncol=2,
        frameon=False,
        fontsize=FONT_SIZE,
        handlelength=2.4,
        columnspacing=2.8,
        handletextpad=0.7,
        labelcolor=TEXT,
    )

    for line in legend.get_lines():
        line.set_linewidth(1.8)

    axis.margins(x=0.03, y=0.05)

    return _TRAJECTORY_MARGINS


def _plot_state(
    figure: Figure,
    results: dict[str, Any] | None,
    series_index: int,
) -> _Margins:
    """Desenha a grandeza física selecionada em função do tempo."""

    if results is None:
        return _plot_placeholder(
            figure,
            "Run a simulation to display physical data.",
        )

    series_index = max(0, min(series_index, len(_STATE_SERIES) - 1))
    _, key, scale, ylabel = _STATE_SERIES[series_index]

    try:
        times = np.asarray(results["trajectory_times"], dtype=float) / DAY_S
        values = np.asarray(results[key], dtype=float) * scale
    except (KeyError, TypeError, ValueError):
        return _plot_placeholder(figure, "Physical data unavailable.")

    count = min(times.size, values.size)

    if count == 0:
        return _plot_placeholder(figure, "No data.")

    times = times[:count]
    values = values[:count]

    valid = np.isfinite(times) & np.isfinite(values)
    times = times[valid]
    values = values[valid]

    if times.size == 0:
        return _plot_placeholder(figure, "No valid physical data.")

    figure.clear()
    figure.patch.set_facecolor(BACKGROUND)

    axis = figure.add_subplot(111)
    _style_axis(axis)

    axis.plot(
        times,
        values,
        color=STATE_COLOR,
        linewidth=1.3,
    )

    axis.set_xlabel("TIME [DAYS]", fontsize=FONT_SIZE, labelpad=2.0)
    axis.set_ylabel(_format_ylabel(ylabel), fontsize=FONT_SIZE, labelpad=2.0)
    axis.margins(x=0.0, y=0.08)

    return _STATE_MARGINS


def _describe_widget(widget: QWidget) -> str:
    policy = widget.sizePolicy()
    layout = widget.layout()
    geometry = widget.geometry()
    hint = widget.sizeHint()

    return (
        f"{type(widget).__name__}(name={widget.objectName()!r}) "
        f"geom={geometry.width()}x{geometry.height()} "
        f"hint={hint.width()}x{hint.height()} "
        f"min={widget.minimumWidth()}x{widget.minimumHeight()} "
        f"max={widget.maximumWidth()}x{widget.maximumHeight()} "
        f"policy={policy.horizontalPolicy()}/{policy.verticalPolicy()} "
        f"layout={type(layout).__name__ if layout is not None else None}"
    )


def _dump_widget_chain(widget: QWidget) -> None:
    """Imprime o widget, seus ancestrais e os itens dos layouts pais."""

    print(f"[ORBITAL] {_BUILD}")
    print(f"[ORBITAL] arquivo carregado: {__file__}")

    depth = 0

    while widget is not None and depth < 10:
        indent = "  " * depth
        print(f"[ORBITAL] {indent}{_describe_widget(widget)}")

        parent = widget.parentWidget()
        layout = parent.layout() if parent is not None else None

        if layout is not None:
            for index in range(layout.count()):
                item = layout.itemAt(index)
                child = item.widget()

                if child is not None:
                    kind = type(child).__name__
                elif item.spacerItem() is not None:
                    kind = "SPACER"
                else:
                    kind = "sub-layout"

                stretch = layout.stretch(index)

                print(
                    f"[ORBITAL] {indent}   item {index}: {kind} "
                    f"stretch={stretch} alignment={item.alignment()}"
                )

        widget = parent
        depth += 1


class _PlotCanvas(FigureCanvas):
    """Canvas cujo tamanho preferencial não domina o layout."""

    def sizeHint(self) -> QSize:
        return QSize(320, 180)

    def minimumSizeHint(self) -> QSize:
        return QSize(160, 100)


class AnalysisPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.results: dict[str, Any] | None = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self._debug_done = False
        self._state_index = 0
        self._trajectory_margins = _PLACEHOLDER_MARGINS
        self._state_margins = _PLACEHOLDER_MARGINS

        self._build_interface()
        self._draw_trajectory()
        self._draw_state()

    def showEvent(self, event) -> None:
        super().showEvent(event)

        if _DEBUG_LAYOUT and not self._debug_done:
            self._debug_done = True
            QTimer.singleShot(400, self._print_layout_debug)

    def _print_layout_debug(self) -> None:
        try:
            _dump_widget_chain(self)

            for card in self.findChildren(QFrame, "analysis_card"):
                print(f"[ORBITAL] cartão: {_describe_widget(card)}")
        except Exception as error:  # noqa: BLE001
            # Diagnóstico auxiliar: falhas aqui não devem interromper a interface.
            print(f"[ORBITAL] falha no diagnóstico: {error!r}")

    def _build_interface(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        layout.addWidget(self._create_trajectory_section(), 5)
        layout.addWidget(self._create_state_section(), 4)

    def _create_panel(self) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame()
        panel.setObjectName("analysis_card")
        panel.setStyleSheet(_CARD_STYLE)
        panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        return panel, layout

    def _create_title(self, text: str) -> QLabel:
        title = QLabel(text)
        title.setObjectName("section_title")
        title.setStyleSheet(_PANEL_TITLE_STYLE)
        title.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

        title.ensurePolished()
        title.setMinimumWidth(title.sizeHint().width())

        return title

    def _create_canvas(self) -> tuple[Figure, _PlotCanvas]:
        figure = Figure(
            figsize=(8, 4),
            dpi=100,
            facecolor=BACKGROUND,
        )

        canvas = _PlotCanvas(figure)
        canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        canvas.setContentsMargins(0, 0, 0, 0)

        return figure, canvas

    def _create_trajectory_section(self) -> QWidget:
        panel, layout = self._create_panel()
        layout.addWidget(self._create_title("TRAJECTORY"))

        self.trajectory_figure, self.trajectory_canvas = self._create_canvas()
        self.trajectory_canvas.setMinimumHeight(180)
        self.trajectory_canvas.mpl_connect(
            "resize_event",
            self._on_trajectory_resize,
        )

        layout.addWidget(self.trajectory_canvas, 1)

        return panel

    def _create_state_section(self) -> QWidget:
        panel, layout = self._create_panel()

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(10)
        header.addWidget(self._create_title("PHYSICAL STATE"))

        self.state_buttons = QButtonGroup(self)
        self.state_buttons.setExclusive(True)
        self._state_buttons: list[QPushButton] = []

        for index, (label, _, _, _) in enumerate(_STATE_SERIES):
            button = self._create_state_button(label, index)
            self._state_buttons.append(button)
            header.addWidget(button, 1)

        layout.addLayout(header)

        self.state_figure, self.state_canvas = self._create_canvas()
        self.state_canvas.setMinimumHeight(140)
        self.state_canvas.mpl_connect(
            "resize_event",
            self._on_state_resize,
        )

        layout.addWidget(self.state_canvas, 1)
        self.state_buttons.idClicked.connect(self._on_state_changed)

        self.distance_button = self._state_buttons[0]
        self.velocity_button = self._state_buttons[1]
        self.energy_button = self._state_buttons[2]
        self.angular_momentum_button = self._state_buttons[3]

        self.distance_button.setChecked(True)

        return panel

    def _create_state_button(
        self,
        text: str,
        button_id: int,
    ) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("analysis_selector")
        button.setCheckable(True)
        button.setMinimumHeight(26)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        button.ensurePolished()
        button.setMinimumWidth(
            button.fontMetrics().horizontalAdvance(text) + 2 * len(text) + 56
        )

        self.state_buttons.addButton(button, button_id)

        return button

    def set_results(self, results: dict[str, Any]) -> None:
        self.results = results
        self._draw_trajectory()
        self._draw_state()

    def _on_state_changed(self, button_id: int) -> None:
        self._state_index = button_id
        self._draw_state()

    def _on_trajectory_resize(self, _event) -> None:
        _apply_margins(self.trajectory_figure, self._trajectory_margins)

    def _on_state_resize(self, _event) -> None:
        _apply_margins(self.state_figure, self._state_margins)

    def _draw_trajectory(self) -> None:
        self._trajectory_margins = _plot_trajectory(
            self.trajectory_figure,
            self.results,
        )
        _apply_margins(self.trajectory_figure, self._trajectory_margins)
        self.trajectory_canvas.draw_idle()

    def _draw_state(self) -> None:
        self._state_margins = _plot_state(
            self.state_figure,
            self.results,
            self._state_index,
        )
        _apply_margins(self.state_figure, self._state_margins)
        self.state_canvas.draw_idle()

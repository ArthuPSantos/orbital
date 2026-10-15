
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class GuidePanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("guide_page")

        self._build_interface()

        self.setStyleSheet(
            """
            #guide_page {
                background-color: #080d12;
            }

            #guide_scroll {
                background-color: #080d12;
                border: none;
            }

            #guide_content {
                background-color: #080d12;
            }

            #guide_eyebrow {
                color: #6fa8c9;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 2px;
            }

            #guide_heading {
                color: #e8edf2;
                font-size: 25px;
                font-weight: 500;
            }

            #guide_intro {
                color: #8795a2;
                font-size: 12px;
            }

            #guide_card {
                background-color: #0c1117;
                border: 1px solid #1b252e;
                border-radius: 7px;
            }

            #guide_card_eyebrow {
                color: #6fa8c9;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 1.5px;
            }

            #guide_card_title {
                color: #e6edf3;
                font-size: 16px;
                font-weight: 500;
            }

            #guide_card_body {
                color: #a1adb8;
                font-size: 12px;
            }

            #guide_card_body a {
                color: #78b6d9;
            }

            #guide_card_body strong {
                color: #dce5ec;
                font-weight: 600;
            }

            #guide_card_body code {
                color: #9dc5df;
                background-color: #121a22;
            }

            #guide_callout {
                background-color: #101820;
                border: 1px solid #263541;
                border-left: 3px solid #5fa8d3;
                border-radius: 5px;
            }

            #guide_callout_title {
                color: #dce5ec;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
            }

            #guide_callout_body {
                color: #9ba9b5;
                font-size: 11px;
            }

            #guide_footer {
                color: #53616d;
                font-size: 9px;
                letter-spacing: 1px;
            }

            QScrollBar:vertical {
                background-color: #080d12;
                width: 9px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #263541;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #3a4c5b;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )

    def _build_interface(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 8, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setObjectName("guide_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("guide_content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(22, 22, 22, 24)
        content_layout.setSpacing(22)

        header = self._create_header()
        content_layout.addWidget(header)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        cards = [
            self._create_card(
                "01 / GETTING STARTED",
                "Run your first experiment",
                """
                <p>ORBITAL lets you configure a two-body gravitational
                system and observe its numerical evolution.</p>

                <p><strong>1. Configure the system.</strong><br>
                In <strong>LABORATORY</strong>, set the primary and
                secondary masses, initial separation, orbital velocity,
                duration, precision and animation speed.</p>

                <p><strong>2. Run the simulation.</strong><br>
                Press <strong>PLAY</strong>. The simulation is calculated
                and the resulting trajectory is displayed on the canvas.</p>

                <p><strong>3. Control playback.</strong><br>
                Use <strong>PAUSE</strong> to stop the animation and
                <strong>RESET</strong> to return to the beginning of the
                calculated trajectory.</p>

                <p><strong>4. Inspect the results.</strong><br>
                Open <strong>ANALYSIS</strong> to examine the trajectory
                and physical quantities over time.</p>
                """,
            ),
            self._create_card(
                "02 / PHYSICAL MODEL",
                "What is being simulated?",
                """
                <p>The simulation models two bodies interacting through
                Newtonian gravitational attraction in two spatial
                dimensions.</p>

                <p><strong>Gravitational force</strong><br>
                The magnitude of the force between two bodies is</p>

                <p align="center">
                F = G m₁m₂ / r²
                </p>

                <p>Here, G is the gravitational constant, m₁ and m₂ are
                the body masses, and r is the distance between them.</p>

                <p><strong>Orbital motion</strong><br>
                The gravitational force changes the bodies' velocities
                and positions over time. The initial velocity strongly
                influences whether the resulting path resembles a
                circular orbit, an elliptical orbit or another trajectory.</p>

                <p><strong>Numerical integration</strong><br>
                ORBITAL uses the Velocity Verlet integration method.
                It advances the system in discrete time steps and is
                commonly used for mechanical systems because of its
                favorable long-term energy behavior.</p>

                <p><strong>Center of mass</strong><br>
                The center of mass is the mass-weighted average position
                of the bodies. Both bodies can move around this point;
                the more massive body generally moves less.</p>
                """,
            ),
            self._create_card(
                "03 / PARAMETERS & UNITS",
                "Understanding the inputs",
                """
                <p><strong>Primary mass</strong><br>
                The mass of the central body. The interface supports
                solar masses and kilograms.</p>

                <p><strong>Secondary mass</strong><br>
                The mass of the orbiting body. Available units include
                Earth masses, solar masses and kilograms.</p>

                <p><strong>Initial distance</strong><br>
                The initial separation between the bodies. It can be
                expressed in astronomical units (AU), kilometers (km)
                or meters (m).</p>

                <p><strong>Initial velocity</strong><br>
                The secondary body's initial speed, expressed in
                kilometers per second (km/s) or meters per second (m/s).
                In the current model, the initial velocity is applied
                perpendicular to the initial separation.</p>

                <p><strong>Duration</strong><br>
                The simulated time span. The interface supports years,
                months, days and hours. The simulation duration is
                converted internally to seconds.</p>

                <p><strong>Animation speed</strong><br>
                Controls how quickly the calculated trajectory is
                played back on screen. It does not change the physical
                parameters or the integration step size.</p>

                <p><strong>Precision</strong><br>
                FAST uses a one-day step, BALANCED uses a six-hour step,
                and HIGH uses a one-hour step. Smaller steps usually
                improve temporal resolution but require more calculations.
                CUSTOM currently uses the six-hour default step.</p>
                """,
            ),
            self._create_card(
                "04 / TRAJECTORY",
                "Reading the orbital plot",
                """
                <p>The trajectory view plots the positions of the bodies
                in the X/Y plane. It provides a spatial view of the
                calculated motion.</p>

                <p><strong>Star trajectory</strong><br>
                Shows the path of the primary body.</p>

                <p><strong>Planet trajectory</strong><br>
                Shows the path of the secondary body.</p>

                <p><strong>Axes and units</strong><br>
                Positions are presented in astronomical units (AU).
                One AU is approximately 149.6 million kilometers.</p>

                <p><strong>What to look for</strong><br>
                Examine the shape and scale of the orbit, how the
                trajectories relate to each other, and whether the
                primary body moves around the system's center of mass.</p>

                <p>The plotted path is the numerical result for the
                configured initial conditions. It is not automatically
                a fit to observed astronomical data.</p>
                """,
            ),
            self._create_card(
                "05 / PHYSICAL STATE",
                "Quantities plotted over time",
                """
                <p>The <strong>PHYSICAL STATE</strong> plot displays one
                selected quantity as a function of time. Use its selector
                to switch between the available series.</p>

                <p><strong>DISTANCE — AU</strong><br>
                The separation between the bodies. Changes in distance
                indicate that the orbit is not perfectly circular.</p>

                <p><strong>VELOCITY — km/s</strong><br>
                The magnitude of the secondary body's velocity.
                Orbital speed generally changes as the distance from
                the primary body changes.</p>

                <p><strong>ENERGY — J</strong><br>
                The total mechanical energy of the system, including
                kinetic and gravitational potential energy. In an ideal
                isolated Newtonian system, total energy is conserved.</p>

                <p><strong>ANGULAR MOMENTUM</strong><br>
                The system's total angular momentum. For an isolated
                system acted on only by internal central gravitational
                forces, total angular momentum is conserved.</p>

                <p>Use these plots to look for trends, unexpected jumps
                and numerical drift over the simulated time span.</p>
                """,
            ),
            self._create_card(
                "06 / NUMERICAL METRICS",
                "How to interpret the results",
                """
                <p><strong>ENERGY ERROR</strong><br>
                The relative difference between the initial and final
                total energy. A smaller value generally indicates less
                energy drift during the calculation.</p>

                <p><strong>ANGULAR MOMENTUM</strong><br>
                The metric shown in the Laboratory summary is the
                relative angular momentum error, despite the shorter
                label. A smaller value indicates better conservation
                between the initial and final states.</p>

                <p><strong>COMPUTATION TIME</strong><br>
                The time required to calculate the simulation steps.
                This is different from the time required to play back
                the animation.</p>

                <p><strong>STEPS</strong><br>
                The number of integration steps calculated for the
                experiment. Longer durations and smaller integration
                steps generally result in more steps.</p>

                <p><strong>Relative error</strong><br>
                For a nonzero initial quantity, the reported error is
                calculated as the absolute difference between final
                and initial values divided by the absolute initial value.</p>

                <p>These conservation errors measure numerical drift;
                they do not measure the difference between the simulated
                orbit and a real planet's observed orbit.</p>
                """,
            ),
        ]

        for index, card in enumerate(cards):
            row = index // 2
            column = index % 2
            grid.addWidget(card, row, column)

        content_layout.addLayout(grid)

        note = self._create_callout(
            "INTERPRETATION NOTE",
            """
            Results depend on the initial conditions, physical model,
            integration step and simulated duration. A smaller numerical
            error is useful, but does not by itself prove that a model
            accurately represents a real astronomical system.
            """,
        )

        content_layout.addWidget(note)

        footer = QLabel(
            "ORBITAL  /  COMPUTATIONAL GRAVITATIONAL LABORATORY"
        )
        footer.setObjectName("guide_footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(footer)

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

    def _create_header(self) -> QWidget:
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(9)

        eyebrow = QLabel("DOCUMENTATION  /  USER GUIDE")
        eyebrow.setObjectName("guide_eyebrow")

        title = QLabel("Understand the system.")
        title.setObjectName("guide_heading")
        title.setWordWrap(True)

        intro = QLabel(
            "A practical reference to configuring experiments, "
            "understanding the physics and interpreting numerical results."
        )
        intro.setObjectName("guide_intro")
        intro.setWordWrap(True)

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(intro)

        return header

    def _create_card(
        self,
        eyebrow_text: str,
        title_text: str,
        body_html: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("guide_card")
        card.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 19, 20, 20)
        layout.setSpacing(11)

        eyebrow = QLabel(eyebrow_text)
        eyebrow.setObjectName("guide_card_eyebrow")

        title = QLabel(title_text)
        title.setObjectName("guide_card_title")
        title.setWordWrap(True)

        body = QLabel(body_html)
        body.setObjectName("guide_card_body")
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setWordWrap(True)
        body.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        body.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addStretch()

        return card

    def _create_callout(
        self,
        title_text: str,
        body_text: str,
    ) -> QFrame:
        callout = QFrame()
        callout.setObjectName("guide_callout")

        layout = QVBoxLayout(callout)
        layout.setContentsMargins(17, 14, 17, 14)
        layout.setSpacing(6)

        title = QLabel(title_text)
        title.setObjectName("guide_callout_title")

        body = QLabel(body_text)
        body.setObjectName("guide_callout_body")
        body.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(body)

        return callout

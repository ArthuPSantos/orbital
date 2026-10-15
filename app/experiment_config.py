from dataclasses import dataclass

from units import (
    distance_to_m,
    duration_to_seconds,
    mass_to_kg,
    velocity_to_m_per_s,
)


@dataclass(frozen=True)
class ExperimentConfig:
    star_mass: float
    star_mass_unit: str

    planet_mass: float
    planet_mass_unit: str

    distance: float
    distance_unit: str

    velocity: float
    velocity_unit: str

    duration: float
    duration_unit: str

    precision: str

    @property
    def star_mass_kg(self) -> float:
        return mass_to_kg(
            self.star_mass,
            self.star_mass_unit,
        )

    @property
    def planet_mass_kg(self) -> float:
        return mass_to_kg(
            self.planet_mass,
            self.planet_mass_unit,
        )

    @property
    def distance_m(self) -> float:
        return distance_to_m(
            self.distance,
            self.distance_unit,
        )

    @property
    def velocity_m_per_s(self) -> float:
        return velocity_to_m_per_s(
            self.velocity,
            self.velocity_unit,
        )

    @property
    def duration_s(self) -> float:
        return duration_to_seconds(
            self.duration,
            self.duration_unit,
        )
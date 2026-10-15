SOLAR_MASS_KG = 1.989e30
EARTH_MASS_KG = 5.972e24

AU_M = 1.495978707e11

KM_M = 1_000.0

YEAR_S = 31_557_600.0
MONTH_S = 2_629_800.0
DAY_S = 86_400.0
HOUR_S = 3_600.0


def mass_to_kg(
    value: float,
    unit: str,
) -> float:
    if unit == "SOLAR MASSES":
        return value * SOLAR_MASS_KG

    if unit == "EARTH MASSES":
        return value * EARTH_MASS_KG

    if unit == "KG":
        return value

    raise ValueError(
        f"Unsupported mass unit: {unit}"
    )


def distance_to_m(
    value: float,
    unit: str,
) -> float:
    if unit == "AU":
        return value * AU_M

    if unit == "KM":
        return value * KM_M

    if unit == "M":
        return value

    raise ValueError(
        f"Unsupported distance unit: {unit}"
    )


def velocity_to_m_per_s(
    value: float,
    unit: str,
) -> float:
    if unit == "KM/S":
        return value * KM_M

    if unit == "M/S":
        return value

    raise ValueError(
        f"Unsupported velocity unit: {unit}"
    )


def duration_to_seconds(
    value: float,
    unit: str,
) -> float:
    if unit == "YEAR":
        return value * YEAR_S

    if unit == "MONTH":
        return value * MONTH_S

    if unit == "DAY":
        return value * DAY_S

    if unit == "HOUR":
        return value * HOUR_S

    raise ValueError(
        f"Unsupported duration unit: {unit}"
    )
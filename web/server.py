
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "app"
STATIC_DIR = ROOT / "web" / "static"

for directory in (ROOT / "src", APP_DIR):
    path = str(directory)
    if path not in sys.path:
        sys.path.insert(0, path)

from experiment_config import ExperimentConfig
from manual_experiment import run_manual_experiment

app = FastAPI(
    title="ORBITAL Web",
    description="Computational laboratory for gravitational systems",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


class SimulationRequest(BaseModel):
    star_mass: float = Field(default=1.0, gt=0, le=1_000_000)
    star_mass_unit: str = "SOLAR MASSES"

    planet_mass: float = Field(default=1.0, gt=0, le=1_000_000)
    planet_mass_unit: str = "EARTH MASSES"

    distance: float = Field(default=1.0, gt=0, le=1_000_000)
    distance_unit: str = "AU"

    velocity: float = Field(default=29.78, gt=0, le=1_000_000)
    velocity_unit: str = "KM/S"

    duration: float = Field(default=1.0, gt=0, le=1000)
    duration_unit: str = "YEAR"

    precision: str = "BALANCED"


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "application": "ORBITAL Web"}


@app.post("/api/simulate")
def simulate(request: SimulationRequest):
    allowed_units = {
        "star_mass_unit": {"SOLAR MASSES", "KG"},
        "planet_mass_unit": {"EARTH MASSES", "SOLAR MASSES", "KG"},
        "distance_unit": {"AU", "KM", "M"},
        "velocity_unit": {"KM/S", "M/S"},
        "duration_unit": {"YEAR", "MONTH", "DAY", "HOUR"},
    }

    values = request.model_dump()

    for field, allowed in allowed_units.items():
        if values[field] not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Unsupported {field}: {values[field]}",
            )

    if request.precision not in {"FAST", "BALANCED", "HIGH", "CUSTOM"}:
        raise HTTPException(
            status_code=422,
            detail="Unsupported precision",
        )

    try:
        config = ExperimentConfig(**values)

        estimated_steps = int(
            config.duration_s
            / {
                "FAST": 86400.0,
                "BALANCED": 21600.0,
                "HIGH": 3600.0,
                "CUSTOM": 21600.0,
            }[config.precision]
        )

        if estimated_steps > 200_000:
            raise HTTPException(
                status_code=422,
                detail="Simulation exceeds the 200,000-step limit. "
                "Reduce the duration or choose a faster precision.",
            )

        result = run_manual_experiment(config)

        return {
            "steps": result["steps"],
            "computation_time": result["computation_time"],
            "energy_error": result["energy_error"],
            "angular_momentum_error": result["angular_momentum_error"],
            "trajectory_star": result["trajectory_star"].tolist(),
            "trajectory_planet": result["trajectory_planet"].tolist(),
            "trajectory_velocity": result["trajectory_velocity"].tolist(),
            "trajectory_times": result["trajectory_times"].tolist(),
            "energy_history": result["energy_history"].tolist(),
            "angular_momentum_history": (
                result["angular_momentum_history"].tolist()
            ),
            "distance_history": result["distance_history"].tolist(),
            "velocity_history": result["velocity_history"].tolist(),
        }

    except HTTPException:
        raise
    except (ValueError, OverflowError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {exc}",
        ) from exc

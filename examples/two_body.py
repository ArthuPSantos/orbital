"""
Experimento de dois corpos do ORBITAL.

Este arquivo contém a lógica de execução do experimento.

Os parâmetros configuráveis ficam separados em:

    two_body_config.py

Dessa forma, podemos alterar as condições iniciais sem
modificar o código responsável pela simulação.
"""

import numpy as np

from two_body_config import (
    DT,
    PLANET_MASS,
    PLANET_POSITION,
    PLANET_VELOCITY,
    SIMULATION_DAYS,
    STAR_MASS,
    STAR_POSITION,
    STAR_VELOCITY,
)

from orbital.physics.body import Body
from orbital.physics.total_energy import total_energy
from orbital.simulation.engine import SimulationEngine
from orbital.simulation.state import SimulationState


# ============================================================
# CONSTANTES DO EXPERIMENTO
# ============================================================

SECONDS_PER_DAY = 86_400

# Intervalo entre as medições de energia.
#
# Exemplo:
#
#     ENERGY_SAMPLE_DAYS = 30
#
# significa que registraremos a energia a cada 30 dias.
#
# Isso é diferente do DT.
#
# DT controla a simulação.
#
# ENERGY_SAMPLE_DAYS controla apenas a frequência
# com que observamos a simulação.

ENERGY_SAMPLE_DAYS = 30


# ============================================================
# CONVERSÃO DE TEMPO
# ============================================================

simulation_seconds = (
    SIMULATION_DAYS
    * SECONDS_PER_DAY
)

energy_sample_seconds = (
    ENERGY_SAMPLE_DAYS
    * SECONDS_PER_DAY
)


# ============================================================
# VALIDAÇÃO
# ============================================================

if simulation_seconds % DT != 0:
    raise ValueError(
        "DT deve dividir exatamente a duração da simulação. "
        "Altere SIMULATION_DAYS ou DT no two_body_config.py."
    )

if energy_sample_seconds % DT != 0:
    raise ValueError(
        "ENERGY_SAMPLE_DAYS deve representar uma quantidade "
        "de passos compatível com DT."
    )


# Quantidade total de passos da simulação.

steps = int(
    simulation_seconds / DT
)


# Quantidade de passos entre cada medição de energia.

energy_sample_steps = int(
    energy_sample_seconds / DT
)


# ============================================================
# CRIAÇÃO DOS CORPOS
# ============================================================

star = Body(
    mass=STAR_MASS,
    position=np.array(
        STAR_POSITION,
        dtype=float,
    ),
    velocity=np.array(
        STAR_VELOCITY,
        dtype=float,
    ),
    radius=6.9634e8,
)

planet = Body(
    mass=PLANET_MASS,
    position=np.array(
        PLANET_POSITION,
        dtype=float,
    ),
    velocity=np.array(
        PLANET_VELOCITY,
        dtype=float,
    ),
    radius=6.371e6,
)


# ============================================================
# ESTADO DA SIMULAÇÃO
# ============================================================

state = SimulationState(
    bodies=[star, planet],
)


# ============================================================
# MOTOR DA SIMULAÇÃO
# ============================================================

engine = SimulationEngine(
    state=state,
    dt=DT,
)


# ============================================================
# ESTADO INICIAL
# ============================================================

initial_position = planet.position.copy()

initial_energy = total_energy(
    state.bodies,
)


# ============================================================
# HISTÓRICO DE ENERGIA
# ============================================================
# Guardamos os resultados para analisar o comportamento da
# energia durante toda a simulação.
#
# Cada item será:
#
#     (tempo_em_dias, energia, erro_relativo)

energy_history: list[
    tuple[float, float, float]
] = []

energy_history.append(
    (
        0.0,
        initial_energy,
        0.0,
    )
)


# ============================================================
# INFORMAÇÕES DO EXPERIMENTO
# ============================================================

print("=" * 60)
print("ORBITAL — EXPERIMENTO DE DOIS CORPOS")
print("=" * 60)

print("\nCONFIGURAÇÃO")
print("-" * 60)

print(
    f"Duração: {SIMULATION_DAYS} dias"
)

print(
    f"Intervalo DT: {DT:.0f} segundos"
)

print(
    f"Número de passos: {steps}"
)

print(
    f"Amostragem de energia: "
    f"a cada {ENERGY_SAMPLE_DAYS} dias"
)

print("\nESTADO INICIAL")
print("-" * 60)

print(
    f"Tempo: "
    f"{state.time / SECONDS_PER_DAY:.1f} dias"
)

print(
    "Posição do planeta:",
    planet.position,
)

print(
    "Velocidade do planeta:",
    planet.velocity,
)

print(
    f"Energia total: "
    f"{initial_energy:.6e} J",
)


# ============================================================
# SIMULAÇÃO
# ============================================================

for step in range(1, steps + 1):

    engine.step()

    # Verifica se chegou ao momento de registrar
    # uma nova medição de energia.

    if step % energy_sample_steps == 0:

        current_energy = total_energy(
            state.bodies,
        )

        relative_error = abs(
            (current_energy - initial_energy)
            / initial_energy
        )

        current_time_days = (
            state.time
            / SECONDS_PER_DAY
        )

        energy_history.append(
            (
                current_time_days,
                current_energy,
                relative_error,
            )
        )


# ============================================================
# RESULTADO FINAL
# ============================================================

final_energy = total_energy(
    state.bodies,
)

position_difference = np.linalg.norm(
    planet.position - initial_position,
)

energy_relative_error = abs(
    (final_energy - initial_energy)
    / initial_energy
)


# ============================================================
# HISTÓRICO DE ENERGIA
# ============================================================

print("\nHISTÓRICO DE ENERGIA")
print("-" * 60)

print(
    f"{'Tempo (dias)':>15}"
    f"{'Energia (J)':>25}"
    f"{'Erro relativo':>20}"
)

for (
    time_days,
    energy,
    relative_error,
) in energy_history:

    print(
        f"{time_days:>15.1f}"
        f"{energy:>25.6e}"
        f"{relative_error:>20.6e}"
    )


# ============================================================
# RESULTADO FINAL
# ============================================================

print("\nRESULTADO FINAL")
print("-" * 60)

print(
    f"Tempo: "
    f"{state.time / SECONDS_PER_DAY:.1f} dias"
)

print(
    "Posição do planeta:",
    planet.position,
)

print(
    "Velocidade do planeta:",
    planet.velocity,
)

print(
    f"Distância entre posição inicial e final: "
    f"{position_difference:.6e} m"
)

print(
    f"Erro relativo de energia: "
    f"{energy_relative_error:.6e}"
)

print("\n" + "=" * 60)
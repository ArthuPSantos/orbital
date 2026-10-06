"""
Configuração do experimento de dois corpos do ORBITAL.

Este arquivo funciona como um painel de controle do experimento.

Você pode alterar os valores abaixo para testar diferentes
situações sem precisar modificar a lógica do programa.

Exemplos de coisas que podem ser alteradas:
    - massa dos corpos
    - posição inicial
    - velocidade inicial
    - duração da simulação
    - intervalo de tempo (dt)

Depois de alterar alguma configuração, execute:

    python examples/two_body.py
"""


# ============================================================
# MASSAS
# ============================================================
# Massa dos corpos em quilogramas (kg).
#
# Valores atuais aproximados:
#
#     Sol   = 1.989 × 10³⁰ kg
#     Terra = 5.972 × 10²⁴ kg
#
# Experimente alterar esses valores para observar como a
# diferença de massa influencia o movimento do sistema.

STAR_MASS = 1.989e30
PLANET_MASS = 5.972e24


# ============================================================
# POSIÇÕES INICIAIS
# ============================================================
# Posição inicial de cada corpo em metros (m).
#
# O ORBITAL trabalha atualmente em 2 dimensões.
#
# O formato é:
#
#     [x, y]
#
# Exemplo:
#
#     [1.496e11, 0.0]
#
# significa:
#
#     x = 149,6 bilhões de metros
#     y = 0 metros
#
# Para colocar o planeta acima do eixo X:
#
#     [0.0, 1.496e11]

STAR_POSITION = [0.0, 0.0]

PLANET_POSITION = [1.496e11, 0.0]


# ============================================================
# VELOCIDADES INICIAIS
# ============================================================
# Velocidade inicial em metros por segundo (m/s).
#
# O formato é:
#
#     [vx, vy]
#
# Para uma órbita aproximadamente circular, a velocidade
# deve ser perpendicular à direção entre os corpos.
#
# Exemplo:
#
#     [0.0, 29780.0]
#
# significa:
#
#     vx = 0 m/s
#     vy = 29.780 m/s
#
# Você pode alterar esses valores para experimentar:
#
#     velocidade menor
#         -> órbita mais fechada ou possível queda
#
#     velocidade adequada
#         -> órbita aproximadamente circular
#
#     velocidade maior
#         -> órbita mais aberta ou possível escape

STAR_VELOCITY = [0.0, 0.0]

PLANET_VELOCITY = [0.0, 35_000.0]


# ============================================================
# DURAÇÃO DA SIMULAÇÃO
# ============================================================
# Tempo total que o experimento deverá simular.
#
# A unidade utilizada aqui é DIAS.
#
# Exemplos:
#
#     30   -> aproximadamente 1 mês
#     365  -> aproximadamente 1 ano
#     730  -> aproximadamente 2 anos
#
# O programa converte esse valor para segundos
# automaticamente.

SIMULATION_DAYS = 365


# ============================================================
# INTERVALO DE TEMPO (DT)
# ============================================================
# DT representa quanto tempo passa em cada passo da simulação.
#
# A unidade é SEGUNDO.
#
# Exemplos:
#
#     3600    -> 1 hora
#     21600   -> 6 horas
#     43200   -> 12 horas
#     86400   -> 1 dia
#
# Um DT menor:
#
#     + maior resolução temporal
#     + geralmente maior precisão
#     - mais passos para executar
#     - maior custo computacional
#
# Um DT maior:
#
#     + menos passos
#     + execução mais rápida
#     - menor resolução temporal
#     - pode aumentar o erro numérico
#     - pode comprometer a estabilidade
#
# Para este experimento, 1 dia é um bom ponto inicial.

DT = 21_600.0
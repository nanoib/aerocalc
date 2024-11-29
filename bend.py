import math
from hydraulic import (
    reynolds_number,
    friction_factor,
    dynamic_pressure,
    velocity,
    hydraulic_diameter,
)
from thermophysical import kinematic_viscosity, density


def bend(
    flow,
    temperature,
    angle,
    r0,
    oriented=None,
    height=None,
    width=None,
    diameter=None,
    roughness=0.001,
):
    """
    Рассчитывает потери давления в отводе (повороте воздуховода) по
    Идельчик «Справочник по гидравлическим сопротивлениям», 1992, стр. 277.
    Нужно задать одно из двух: пару height/width или diameter.
    Направление поворота oriented требуется, чтобы правильно определить отношение r0/b0.
    Для круглого воздуховода oriented можно не задавать (не влияет на расчет).

    Аргументы:
    flow - расход воздуха, м^3/ч
    temperature - Температура воздуха, °C
    angle - угол поворота воздуховода, градусы
    r0 - радиус отвода, м
    oriented - направление поворота воздуховода (vert - вертикально, horiz - горизонтально)
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м
    roughness - абсолютная шероховатость, м

    Возвращает:
    Потери давления на трение, Па
    """
    print("================================")
    print(
        f"Расчет отвода с параметрами\nflow: {flow} м^3/ч, height: {height} м, width:\
{width} м, diameter: {diameter} м, temperature: {temperature} °C\n"
    )

    # Проверка, что задана либо оба из пары height/width, либо диаметр
    assert not (
        (height or width) and diameter
    ), "Необходимо указать одно из двух: пару height/width или diameter."
    assert not (
        ((height is None) or (width is None)) and (diameter is None)
    ), "Не указана ни пара height/width, ни diameter."
    assert (height and width) or diameter, "Неправильно указаны геометрические характеристики"

    # Проверка, что ориентация имеет одно из допустимых значений
    assert (
        (oriented == "horiz") or (oriented == "vert") or (oriented is None)
    ), "Неправильно указана ориентация отвода"

    # Проверка, что некруглому отводу задана ориентация
    assert ((diameter is None) and (oriented == "horiz" or oriented == "vert")) or (
        diameter is not None
    ), "Неправильно указана ориентация отвода"

    # Рассчитываем динамическое давление
    p_dyn = dynamic_pressure(density(temperature), velocity(flow, height, width, diameter))

    # Рассчитываем гидравлический диаметр
    d_hyd = hydraulic_diameter(height, width, diameter)

    # Рассчитываем скорость воздуха
    v = velocity(flow, height, width, diameter)

    # Рассчитываем критерий Рейнольдса
    re = reynolds_number(v, d_hyd, kinematic_viscosity(temperature))

    # Рассчитываем коэффициент гидравлического сопротивления трения
    lmbd = friction_factor(re, d_hyd, roughness)

    # TODO в программе не учитывается k_delta и k_re
    k_delta = 1 if re < 40000 else 2
    k_re = 1.3 - 0.29 * math.log(re * 10**-5)

    # TODO вероятно в программе не учитываются разница ориентации отвода (т.е. фактические a0, b0)
    r0b0 = r0 / diameter if diameter else (r0 / width if oriented == "horiz" else r0 / height)
    a0b0 = None if diameter else (height / width if oriented == "horiz" else width / height)

    A1 = 0.9 * math.sin(angle) if angle < 70 else ((0.7 + 0.35 * angle / 90) if angle > 100 else 1)
    B1 = 0.21 * (r0b0) ** (-2.5 if r0b0 <= 1 else -0.5)
    C1 = 1 if diameter else (0.85 + 0.125 / a0b0 if height / width <= 4 else 1.115 - 0.84 / a0b0)

    ksi_local = A1 * B1 * C1
    ksi_friction = 0.0175 * angle * lmbd * r0 / d_hyd
    ksi = k_delta * k_re * ksi_local + ksi_friction

    print(
        f"Расчетные параметры:\nr0/b0: {r0b0:.2f}, k_delta: {k_delta:.2f}, \
k_re: {k_re:.2f}, A1: {A1:.2f}, B1: {B1:.2f}, C1: {C1:.2f}\nksi: {ksi:.2f}"
    )

    result = ksi * p_dyn
    print(f"Потери давления на трение: {result:.3f} Па")


bend(
    flow=1000,
    temperature=-25,
    angle=90,
    oriented="horiz",
    r0=0.25,
    height=0.3,
    width=0.3,
)
bend(
    flow=1000,
    temperature=-25,
    angle=90,
    oriented="horiz",
    r0=0.25,
    height=0.3,
    width=0.6,
)

bend(flow=600, temperature=-25, angle=90, r0=0.185, diameter=0.16)

import math
from physics.hydraulic import (
    reynolds_number,
    friction_factor,
    dynamic_pressure,
    velocity,
    hydraulic_diameter,
)
from physics.thermophysical import (
    kinematic_viscosity_idelchik,
    kinematic_viscosity_thermo,
    density_mendeleev,
    density_thermo,
)


def elbow(
    flow,
    temperature,
    angle,
    r0,
    oriented=None,
    height=None,
    width=None,
    diameter=None,
    roughness=0.0015,
    thermophysics="idelchik",
    calcversion=None,
):
    """
    Рассчитывает потери давления в отводе (повороте воздуховода) по
    Идельчик «Справочник по гидравлическим сопротивлениям», 1992, стр. 277.
    Нужно задать одно из двух: пару height/width или diameter.
    Направление поворота oriented требуется, чтобы правильно определить отношение r0/b0.
    Для круглого воздуховода oriented можно не задавать (не влияет на расчет).
    Шероховатость по умолчанию 1.5 мм

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
    thermophysics - модель термофизических свойств (idelchik или thermo)
    calcversion - версия расчета. "22" - версия без kdelta и kre

    Возвращает:
    Потери давления на трение, Па
    """
    print("================================")
    print(
        f"Расчет отвода с параметрами\nflow: {flow} м^3/ч, height: {height} м, width:\
{width} м, diameter: {diameter} м, temperature: {temperature} °C\n"
    )

    ###########Проверки#############
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
    ###########Проверки#############

    # Получаем термофизические данные
    if thermophysics == "idelchik":
        kinematic_viscosity = kinematic_viscosity_idelchik
        density = density_mendeleev
    elif thermophysics == "thermo":
        kinematic_viscosity = kinematic_viscosity_thermo
        density = density_thermo
    else:
        raise ValueError("Неизвестный вид термофизических данных")

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
    if calcversion == "22":
        print("Расчет по версии 22 без k_delta и k_re")
        k_delta = 1
        k_re = 1
    elif calcversion is None:
        k_delta = 1 if re < 40000 else 2
        k_re = 1.3 - 0.29 * math.log(re * 10**-5)
    else:
        raise ValueError("Неизвестная версия расчета")

    # TODO вероятно в программе не учитываются разница ориентации отвода (т.е. фактические a0, b0)
    r0b0 = r0 / diameter if diameter else (r0 / width if oriented == "horiz" else r0 / height)
    a0b0 = None if diameter else (height / width if oriented == "horiz" else width / height)

    A1 = (
        0.9 * math.sin(math.radians(angle))
        if angle < 70
        else ((0.7 + 0.35 * angle / 90) if angle > 100 else 1)
    )
    B1 = 0.21 * (r0b0) ** (-2.5 if r0b0 <= 1 else -0.5)
    C1 = 1 if diameter else (0.85 + 0.125 / a0b0) if height / width <= 4 else (1.115 - 0.84 / a0b0)

    dzeta_local = A1 * B1 * C1
    dzeta_friction = 0.0175 * angle * lmbd * r0 / d_hyd
    dzeta = k_delta * k_re * dzeta_local + dzeta_friction

    print(
        f"Расчетные параметры:\nr0/b0: {r0b0:.2f}, k_delta: {k_delta:.2f}, \
k_re: {k_re:.3f}, A1: {A1:.3f}, B1: {B1:.3f}, C1: {C1:.3f}\ndzeta: {dzeta:.3f}"
    )

    result = dzeta * p_dyn
    print(f"Полные dP в отводе: {result:.3f} Па")
    print("================================")

    return result

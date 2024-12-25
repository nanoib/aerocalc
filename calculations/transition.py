import math
from physics.hydraulic import (
    reynolds_number,
    friction_factor,
    dynamic_pressure,
    hydraulic_diameter,
)
from physics.thermophysical import (
    kinematic_viscosity_idelchik,
    kinematic_viscosity_thermo,
    density_mendeleev,
    density_thermo,
)


def transition(
    flow,
    temperature,
    diameter1=None,
    height1=None,
    width1=None,
    diameter2=None,
    height2=None,
    width2=None,
    length=None,
    roughness=0.001,
    thermophysics="idelchik",
    calcversion=None,
):
    """
    Рассчитывает потери давления в переходе воздуховода.
    По: Идельчик «Справочник по гидравлическим сопротивлениям», 1992,
    стр. 192 (5-5, 5-6).
    Индекс 1 относится к первому сечению (по ходу среды),
    индекс 2 относится ко второму сечению (по ходу среды).
    Нужно задать:
    (пару height1/width1 или diameter1) И (пару height1/width1 или diameter1).

    Аргументы:
    flow - расход воздуха, м^3/ч
    temperature - температура воздуха, °C
    height1 - высота перехода, м
    width1 - ширина перехода, м
    diameter1 - диаметр, м
    height2 - высота перехода, м
    width2 - ширина перехода, м
    diameter2 - диаметр, м
    length - длина перехода, м
    roughness - абсолютная шероховатость, м
    thermophysics - модель термофизических свойств (idelchik или thermo)
    calcversion - версия расчета. "22" - расчет по версии 22

    Возвращает:
    Потери давления на трение, Па
    """

    print("================================")
    print(
        f"Расчет перехода с параметрами\nflow: {flow} м^3/ч, length: {length} м, height1: {height1} м, width1: {width1} м, diameter1: {diameter1} м, height2: {height2} м, width2: {width2} м, diameter2: {diameter2} м, temperature: {temperature} °C\n"
    )

    ###########Проверки#############
    # Проверка, что задана либо оба из пары height/width, либо диаметр
    assert not (
        (height1 or width1) and diameter1
    ), "Необходимо указать одно из двух: пару height1/width1 или diameter1."
    assert not (
        ((height1 is None) or (width1 is None)) and (diameter1 is None)
    ), "Не указана ни пара height1/width1, ни diameter1."
    assert (height1 and width1) or diameter1, "Неправильно указаны геометрические характеристики"
    # То же для сечения 2
    assert not (
        (height2 or width2) and diameter2
    ), "Необходимо указать одно из двух: пару height1/width1 или diameter1."
    assert not (
        ((height2 is None) or (width2 is None)) and (diameter2 is None)
    ), "Не указана ни пара height1/width1, ни diameter1."
    assert (height2 and width2) or diameter2, "Неправильно указаны геометрические характеристики"
    ###########Проверки#############

    # 1. Рассчитывыем коэффициент сопротивления расширения перехода

    # Рассчитываем полуугол перехода. Поскольку неизвестно заранее, какие из
    # габаритов заданы, а также неизвестно, по ширине или по высоте происходит
    # расширение, проверяются все возможные варианты и берется наибольшая дельта

    # Поиск максимальной дельты между габаритами перехода
    delta = 0

    # Поскольку неизвестно, будет ли задана высота-ширина или диаметр, проверяем все
    for dim1 in [height1, width1, diameter1]:
        if dim1 is None:
            # Если параметр не задан (т.е. он None), то пропускаем его
            continue
        else:
            for dim2 in [height2, width2, diameter2]:
                if dim2 is None:
                    # Если параметр не задан (т.е. он None), то пропускаем его
                    continue
                else:
                    # Если пара габаритов для двух сечений нашлась, то вычисляем дельту
                    delta_current = abs(dim2 - dim1)
                # Если текущая дельта больше предыдущей, она становится максимальной
                if delta_current > delta:
                    delta = delta_current
    print(f"Дельта между сечениями перехода: {delta:.3f}")

    # Непосредственно расчет полуугла перехода
    alfa05 = math.atan(delta / 2 / length)

    # Коэффициент степени расширения перехода
    # Площади сечения перехода
    def square(height, width, diameter):
        return height * width if height and width else math.pi * diameter**2 / 4

    s1 = square(height1, width1, diameter1)
    s2 = square(height2, width2, diameter2)
    # Непосредственно степень расширения перехода
    np = s1 / s2 if s1 > s2 else s2 / s1

    # Местный коэффициент сопротивления перехода
    if s2 >= s1:
        # Если расширение
        dzeta_transition = 3.2 * (math.tan(alfa05) ** 1.25) * (1 - 1 / np) ** 2
    else:
        # Если сужение
        if calcversion == "22":
            print("Расчет по версии 22 без местных потерь на сужении")
            dzeta_transition = 0
        elif calcversion is None:
            # Формула 5-136
            # TODO этот коэффициент в программе равен нулю. Не должен
            alpha = alfa05 * 2
            dzeta_transition = (
                -0.0125 * np**4 + 0.0224 * np**3 - 0.00723 * np**2 + 0.00444 * np - 0.00745
            ) * (alpha**3 + 2 * math.pi * alpha**2 - 10 * alpha)
        else:
            raise ValueError("Неизвестная версия расчета")
    print(f"Коэффициент сопротивления расширения перехода: {dzeta_transition:.4f}")

    # 2. Рассчитывыем коэффициент сопротивления трения

    # Получаем термофизические данные
    if thermophysics == "idelchik":
        kinematic_viscosity = kinematic_viscosity_idelchik
        density = density_mendeleev
    elif thermophysics == "thermo":
        kinematic_viscosity = kinematic_viscosity_thermo
        density = density_thermo
    else:
        raise ValueError("Неизвестный вид термофизических данных")

    # Рассчитываем гидравлический диаметр
    d_hyd1 = hydraulic_diameter(height1, width1, diameter1)
    d_hyd2 = hydraulic_diameter(height2, width2, diameter2)

    # Выбираем наименьший гидравлический диаметр как определяющий (для расчета re и lmbd)
    d_hyd_base = min(d_hyd1, d_hyd2)

    # Рассчитываем определяющую (максимальную) скорость воздуха по входном сечению
    # Если сужение
    if calcversion == "22":
        print("Расчет скорости по версии 22, по большему сечению")
        v_base = flow / 3600 / s2
    elif calcversion is None:
        v_base = flow / 3600 / s1
    else:
        raise ValueError("Неизвестная версия расчета")

    # Рассчитываем критерий Рейнольдса по определяющей скорости и минимальному гидр. диаметру
    re = reynolds_number(v_base, d_hyd_base, kinematic_viscosity(temperature))

    # Рассчитываем коэффициент гидравлического сопротивления трения
    lmbd = friction_factor(re, d_hyd_base, roughness)

    # Рассчитываем коэффициент сопротивления трения перехода (формула 5-6)
    dzeta_friction = lmbd / (8 * math.sin(alfa05)) * (1 - 1 / np**2)
    print(f"Коэффициент сопротивления трения перехода: {dzeta_friction:.4f}")

    # 3. Рассчитываем общий коэффициент гидравлического сопротивления расширения и потери
    dzeta = dzeta_friction + dzeta_transition

    # Рассчитываем динамическое давление по определяющей скорости
    p_dyn = dynamic_pressure(density(temperature), v_base)

    print(
        f"Расчетные параметры:\nv_base: {v_base:.2f}, s1: {s1:.5f}, s2: {s2:.5f}, \
np1: {np:.2f}, d_hyd_base: {d_hyd_base:.3f}, alfa05: {alfa05:.3f} рад/{math.degrees(alfa05):.3f}°"
    )

    result = dzeta * p_dyn
    print(f"Полные dP в переходе: {result:.3f} Па")
    print("================================")

    return result

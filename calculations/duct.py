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


# Главная функция для расчета потерь в воздуховоде
def duct(
    flow,
    length,
    temperature,
    height=None,
    width=None,
    diameter=None,
    roughness=0.001,
    thermophysics="idelchik",
):
    """
    Рассчитывает потери давления в воздуховоде по формуле Дарси-Вейсбаха.
    По: Идельчик «Справочник по гидравлическим сопротивлениям», 1992,
    стр. 60 (2-2).
    Нужно задать одно из двух: пару height/width или diameter.

    Аргументы:
    flow - расход воздуха, м^3/ч
    lenght - длина участка воздуховода, м
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м
    temperature - Температура воздуха, °C
    roughness - абсолютная шероховатость, м
    thermophysics - модель термофизических свойств (idelchik или thermo)

    Возвращает:
    Потери давления на трение, Па
    """

    ###########Проверки#############
    assert not (
        (height or width) and diameter
    ), "Необходимо указать одно из двух: пару height/width или diameter."
    assert not (
        ((height is None) or (width is None)) and (diameter is None)
    ), "Не указана ни пара height/width, ни diameter."
    assert (height and width) or diameter, "Неправильно указаны геометрические характеристики"
    ###########Проверки#############

    print("================================")
    print(
        f"Расчет воздуховода с параметрами\nflow: {flow} м^3/ч, length: {length} м, height: {height} м, width: {width} м, diameter: {diameter} м, temperature: {temperature} °C\n"
    )

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
    d_hyd = hydraulic_diameter(height, width, diameter)

    # Рассчитываем скорость воздуха
    v = velocity(flow, height, width, diameter)

    # Рассчитываем критерий Рейнольдса
    re = reynolds_number(v, d_hyd, kinematic_viscosity(temperature))

    # Рассчитываем коэффициент гидравлического сопротивления трения
    lmbd = friction_factor(re, d_hyd, roughness)

    # Рассчитываем динамическое давление
    p_dyn = dynamic_pressure(density(temperature), v)

    # Рассчитываем удельные потери давления на трение (коэф. гидр. сопр.)
    dzeta = lmbd * length / d_hyd
    print(f"Коэффициент гидравлического сопротивления: {dzeta:.3f}")

    # Рассчитываем полные потери давления на трение
    result = p_dyn * dzeta

    print(f"Полные dP в воздуховоде: {result:.3f} Па")
    print("================================")

    return result

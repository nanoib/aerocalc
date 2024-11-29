import math


def reynolds_number(velocity, diameter, kinematic_viscosity):
    """
    Рассчитывает критерий Рейнольдса.

    Аргументы:
    velocity - скорость движения воздуха в воздуховоде, м/с
    diameter - диаметр воздуховода, м
    kinematic_viscosity - кинематическая вязкость воздуха, м^2/с

    Возвращает:
    критерий Рейнольдса
    """
    result = velocity * diameter / kinematic_viscosity
    print(f"Число Рейнольдса: {result:.0f}")
    return result


def friction_factor(reynolds_number, hydraulic_diameter, roughness):
    """
    Рассчитывает коэффициент гидравлического сопротивления трения.

    Аргументы:
    reynolds_number - критерий Рейнольдса
    roughness - абсолютная эквивалентная шероховатость поверхности воздуховода, мм

    Возвращает:
    float - коэффициент гидравлического сопротивления трения
    """
    result = 0.11 * (roughness / hydraulic_diameter + 68 / reynolds_number) ** 0.25
    print(f"Коэффициент гидравлического сопротивления трения: {result:.4f}")
    return result


# Функция для расчета динамического давления
def dynamic_pressure(density, velocity):
    """
    Рассчитывает динамическое давление.

    Аргументы:
    density - плотность воздуха, кг/м^3
    velocity - скорость движения воздуха в воздуховоде, м/с

    Возвращает:
    динамическое давление, Па
    """
    result = 0.5 * density * velocity**2
    print(f"Динамическое давление: {result:.2f} Па")
    return result


def velocity(flow, height=None, width=None, diameter=None):
    """
    Рассчитывает скорость в воздуховоде.
    Нужно задать одно из двух: пару height/width или diameter.

    Аргументы:
    flow - расход воздуха, м^3/ч
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м

    Возвращает:
    скорость, м/c
    """
    if height and width:
        result = flow / 3600 / height / width
    elif diameter:
        result = flow / 3600 / (math.pi * diameter**2 / 4)
    else:
        raise ValueError("Не найдено нужных параметров.")

    print(f"Скорость в воздуховоде: {result:.2f} м/c")

    return result


def hydraulic_diameter(height=None, width=None, diameter=None):
    """
    Рассчитывает гидравлический диаметр воздуховода.
    Нужно задать одно из двух: пару height/width или diameter.

    Аргументы:
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м

    Возвращает:
    гидравлический диаметр, м
    """

    if height and width:
        result = 2 * height * width / (height + width)
    elif diameter:
        result = diameter
    else:
        raise ValueError("Не найдено нужных параметров.")

    print(f"Гидравлический диаметр: {result:.3f} м")

    return result

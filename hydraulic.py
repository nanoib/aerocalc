import math


def reynolds_number(velocity, diameter, kinematic_viscosity):
    """
    Рассчитывает критерий Рейнольдса.

    Аргументы:
    velocity (float) - скорость движения воздуха в воздуховоде, м/с
    diameter (float) - диаметр воздуховода, м
    kinematic_viscosity (float) - кинематическая вязкость воздуха, м^2/с

    Возвращает:
    float - критерий Рейнольдса
    """
    reynolds_number_value = velocity * diameter / kinematic_viscosity
    print(f"Число Рейнольдса: {reynolds_number_value:.0f}")
    return reynolds_number_value


def friction_factor(reynolds_number, hydraulic_diameter, roughness):
    """
    Рассчитывает коэффициент гидравлического сопротивления трения.

    Аргументы:
    reynolds_number (float) - критерий Рейнольдса
    roughness (float) - абсолютная эквивалентная шероховатость поверхности воздуховода, мм

    Возвращает:
    float - коэффициент гидравлического сопротивления трения
    """
    friction_factor_value = (
        0.11 * (roughness / hydraulic_diameter + 68 / reynolds_number) ** 0.25
    )
    print(
        f"Коэффициент гидравлического сопротивления трения: {friction_factor_value:.4f}"
    )
    return friction_factor_value


# Функция для расчета динамического давления
def dynamic_pressure(density, velocity):
    """
    Рассчитывает динамическое давление.

    Аргументы:
    density (float) - плотность воздуха, кг/м^3
    velocity (float) - скорость движения воздуха в воздуховоде, м/с

    Возвращает:
    float - динамическое давление, Па
    """
    pd = 0.5 * density * velocity**2
    print(f"Динамическое давление: {pd:.2f} Па")
    return pd


def velocity(flow, hydraulic_diameter):
    """
    Рассчитывает динамическое давление.

    Аргументы:
    flow (float) - расход воздуха, м^3/ч
    hydraulic_diameter (float) - скорость движения воздуха в воздуховоде, м/с

    Возвращает:
    float - скорость, м/c
    """
    # Рассчитываем скорость движения воздуха
    velocity = flow / 3600 / (math.pi * hydraulic_diameter**2 / 4)
    print(f"Скорость в воздуховоде: {velocity:.1f} м/c")
    return velocity

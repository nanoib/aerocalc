import csv
from thermo.chemical import Mixture


def kinematic_viscosity_thermo(t):
    """
    Возвращает кинематическую вязкость воздуха используя библиотеку thermo.

    Аргументы:
    temperature - температура воздуха, °C

    Возвращает:
    кинематическая вязкость воздуха, м^2/с
    """
    air = Mixture("air", T=t + 273.15, P=101325)
    result = air.mu / air.rho
    print(f"Кинематическая вязкость воздуха по thermo: {result*100000:.3f}*10-5 м^2/с")
    return result


def density_thermo(t):
    """
    Возвращает плотность воздуха используя библиотеку thermo.

    Аргументы:
    temperature - температура воздуха, °C

    Возвращает:
    плотность воздуха, кг/м^3
    """
    air = Mixture("air", T=t + 273.15, P=101325)
    result = air.rho
    print(f"Плотность воздуха по thermo: {result:.3f}, кг/м^3")
    return result


def density_mendeleev(t):
    """
    Рассчитывает плотность воздуха используя уравнения состояния
    идеального газа (уравнение Менделеева-Клапейрона).

    Аргументы:
    temperature - температура воздуха, °C

    Возвращает:
    плотность воздуха, кг/м^3
    """
    pressure = 101325  # Па (1 атм)
    R_constant = 8.314  # Дж/(моль·К)
    T_kelvin = t + 273.15  # Кельвины
    M_air = 0.02898  # кг/моль

    # Calculate density
    result = pressure * M_air / (R_constant * T_kelvin)

    print(f"Плотность воздуха по идеальному газу: {result:.3f}, кг/м^3")
    return result


def kinematic_viscosity_idelchik(t):
    """
    Рассчитывает кинематическую вязкость воздуха интерполяцией
    по: Идельчик «Справочник по гидравлическим сопротивлениям», 1992,
    стр. 17 (табл. 1-7).

    Аргументы:
    temperature - температура воздуха, °C

    Возвращает:
    кинематическая вязкость воздуха, м^2/с
    """

    # Настройка, насколько далеко можно экстраполировать от данных
    extrapolation_max_factor = 2.0

    # Чтение данных из CSV
    with open("./data/kinematic_viscosity.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        temperature_values = []
        physical_values = []
        for row in reader:
            temperature_values.append(float(row["t"]))
            physical_values.append(float(row["kinematic_viscosity"]))

    if t < temperature_values[0]:
        # Экстраполяция вниз диапазона
        closest_range = abs(temperature_values[1] - temperature_values[0])
        extrapolation_range = abs(t - temperature_values[0])
        # Проверка, что значение не слишком далеко от данных
        assert (
            extrapolation_range <= closest_range * extrapolation_max_factor
        ), "Значение слишком далеко от данных"
        slope_below_min = (physical_values[1] - physical_values[0]) / (
            temperature_values[1] - temperature_values[0]
        )
        result = physical_values[0] - slope_below_min * (temperature_values[0] - t)
    elif t > temperature_values[-1]:
        # Экстраполяция вверх диапазона
        closest_range = abs(temperature_values[-1] - temperature_values[-2])
        extrapolation_range = abs(t - temperature_values[-1])
        # Проверка, что значение не слишком далеко от данных
        assert (
            extrapolation_range <= closest_range * extrapolation_max_factor
        ), "Значение слишком далеко от данных"
        slope_below_max = (physical_values[-1] - physical_values[-2]) / (
            temperature_values[-1] - temperature_values[-2]
        )
        result = physical_values[-1] + slope_below_max * (t - temperature_values[-1])
    else:
        # Интерполяция внутри диапазона
        for i in range(len(temperature_values) - 1):
            if temperature_values[i] <= t <= temperature_values[i + 1]:
                slope = (physical_values[i + 1] - physical_values[i]) / (
                    temperature_values[i + 1] - temperature_values[i]
                )
                result = physical_values[i] + slope * (t - temperature_values[i])

    print(
        f"Кинематическая вязкость воздуха по Идельчик при {t}°C: {result * 100000:.3f}*10^-5 m^2/s"
    )
    return result


density_mendeleev(-20)

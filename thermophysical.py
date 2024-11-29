from thermo.chemical import Chemical
from thermo.chemical import Mixture

def kinematic_viscosity(t):
    """
    Рассчитывает кинематическую вязкость воздуха с использованием библиотеки thermo.
    
    Аргументы:
    temperature - температура воздуха, °C
    
    Возвращает:
    кинематическая вязкость воздуха, м^2/с
    """
    air = Mixture('air', T= t + 273.15, P=101325)
    nu = air.mu / air.rho
    print(f"Кинематическая вязкость воздуха: {nu*100000:.3f}*10-5 м^2/с")
    return nu

def density(t):
    """
    Рассчитывает плотность воздуха с использованием библиотеки thermo.
    
    Аргументы:
    temperature - температура воздуха, °C
    
    Возвращает:
    плотность воздуха, кг/м^3
    """
    air = Mixture('air', T= t + 273.15, P=101325)
    rho = air.rho
    print(f"Плотность воздуха: {rho:.3f}, кг/м^3")
    return rho
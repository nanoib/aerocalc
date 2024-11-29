from hydraulic import reynolds_number, friction_factor, dynamic_pressure, velocity
from thermophysical import kinematic_viscosity, density

# Функция для расчета удельных потерь давления на трение
def specific_pressure_loss(friction_factor, diameter, dynamic_pressure):
    """
    Рассчитывает удельные потери давления на трение.
    
    Аргументы:
    friction_factor - коэффициент гидравлического сопротивления трения
    diameter - диаметр воздуховода, м
    dynamic_pressure - динамическое давление, Па
    
    Возвращает:
    удельные потери давления на трение, Па/м
    """
    return friction_factor / diameter * dynamic_pressure

# Функция для расчета потерь давления на трение
def pressure_loss(specific_pressure_loss, length, correction_factor):
    """
    Рассчитывает потери давления на трение.
    
    Аргументы:
    specific_pressure_loss - удельные потери давления на трение, Па/м
    length - длина участка воздуховода, м
    correction_factor - поправочный коэффициент
    
    Возвращает:
    потери давления на трение, Па
    """
    return specific_pressure_loss * length * correction_factor

# Главная функция для расчета потерь в воздуховоде
def duct(flow, height=None, width=None, diameter=None):
    """
    Рассчитывает потери давления в воздуховоде.
    
    Аргументы:
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м
    flow - расход воздуха, м^3/ч
    
    Возвращает:
    Потери давления на трение, Па
    """
    temperature = 0  # Температура воздуха, °C
    roughness = 0.001  # Абсолютная эквивалентная шероховатость поверхности воздуховода, мм
    length = 1.37  # Длина участка воздуховода, м
    correction_factor = 1  # Поправочный коэффициент
    
    # Рассчитываем гидравлический диаметр
    if height and width:
        hydraulic_diameter = 2 * height * width / (height + width)
    else:
        hydraulic_diameter = diameter
    print(f"Гидравлический диаметр: {hydraulic_diameter:.3f} м")

    # Рассчитываем критерий Рейнольдса
    reynolds_number_value = reynolds_number(velocity(flow, hydraulic_diameter), hydraulic_diameter, kinematic_viscosity(temperature))

    # Рассчитываем коэффициент гидравлического сопротивления трения
    friction_factor_value = friction_factor(reynolds_number_value, hydraulic_diameter, roughness)

    # Рассчитываем динамическое давление
    dynamic_pressure_value = dynamic_pressure(density(temperature), velocity(flow, hydraulic_diameter))
    
    # Рассчитываем удельные потери давления на трение
    specific_pressure_loss_value = specific_pressure_loss(friction_factor_value, hydraulic_diameter, dynamic_pressure_value)
    
    # Рассчитываем полные потери давления на трение
    pressure_loss_value = pressure_loss(specific_pressure_loss_value, length, correction_factor)
    
    return pressure_loss_value

# Расчет
pressure_loss = duct(flow=600, diameter=0.16)
print(f"\nПотери давления: {pressure_loss:.2f} Па\n")

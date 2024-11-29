from hydraulic import reynolds_number, friction_factor, dynamic_pressure, velocity, hydraulic_diameter
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
    result = friction_factor / diameter * dynamic_pressure
    print(f"\nУдельные потери давления: {result:.2f} Па")
    return result

# Функция для расчета потерь давления на трение
def pressure_loss(specific_pressure_loss, length):
    """
    Рассчитывает потери давления на трение.
    
    Аргументы:
    specific_pressure_loss - удельные потери давления на трение, Па/м
    length - длина участка воздуховода, м
    
    Возвращает:
    потери давления на трение, Па
    """
    result = specific_pressure_loss * length
    print(f"\nПотери давления: {result:.2f} Па")
    return result

# Главная функция для расчета потерь в воздуховоде
def duct(flow, length, temperature, height=None, width=None, diameter=None):
    """
    Рассчитывает потери давления в воздуховоде. 
    Нужно задать одно из двух: пару height/width или diameter.
    
    Аргументы:
    flow - расход воздуха, м^3/ч
    lenght - длина участка воздуховода, м
    height - высота воздуховода, м
    width - ширина воздуховода, м
    diameter - диаметр воздуховода, м
    temperature - Температура воздуха, °C
    
    Возвращает:
    Потери давления на трение, Па
    """
    print('================================')
    print(f'Расчет воздуховода с параметрами\nflow: {flow} м^3/ч, length: {length} м, height: {height} м, width: {width} м, diameter: {diameter} м, temperature: {temperature} °C\n')
    roughness = 0.001  # Абсолютная эквивалентная шероховатость поверхности воздуховода, мм
    
    # Рассчитываем гидравлический диаметр
    d_hyd = hydraulic_diameter(height, width, diameter)

    # Рассчитываем критерий Рейнольдса
    re = reynolds_number(velocity(flow, height, width, diameter), d_hyd, kinematic_viscosity(temperature))

    # Рассчитываем коэффициент гидравлического сопротивления трения
    lmbd = friction_factor(re, d_hyd, roughness)

    # Рассчитываем динамическое давление
    p_dyn = dynamic_pressure(density(temperature), velocity(flow, height, width, diameter))
    
    # Рассчитываем удельные потери давления на трение
    p_vol = specific_pressure_loss(lmbd, d_hyd, p_dyn)
    
    # Рассчитываем полные потери давления на трение
    result = pressure_loss(p_vol, length)
    print('================================')
    
    return result

# Расчет
duct(flow=600, length=1.37, temperature=0, diameter=0.16)
duct(flow=1000, length=1, temperature=-25, height=0.3, width=0.3)
import math
from physics.hydraulic import (
    velocity,
    dynamic_pressure,
)
from physics.thermophysical import (
    density_mendeleev,
    density_thermo,
)


def velocity_best_mixture(flow_o1, v_o1, angle_o1, flow_o2, v_o2, angle_o2, flow_p, v_p, flow_c):
    """
    Рассчитывает наивыгоднейшую скорость смешивания .
    По: Формуле из "Расчеты в nanoCAD BIM Вентиляция"
    Индекс «c» относится к смесительному патрубку (магистральный патрубок с суммарным расходом).
    Индекс «o1» относится к ответвлению тройника или к первому из боковых ответвлений крестовины.
    Индекс «o2» относится ко второму боковому ответвлению крестовины.
    Индекс «p» («п») относится к проходу (магистральный патрубок с частичным расходом).
    Если расчет ведется для тройника, то flow_o2, v_o2, angle_o2 нужно задать равными «None».
    Аргументы обозначаются как в функции tee().
    """
    ###########Проверки#############
    # Проверяем, заданы ли необходимые параметры
    assert (
        flow_o1 and v_o1 and angle_o1 and flow_p and v_p and flow_c
    ), "Не заданы нужные параметры!"
    ###########Проверки#############

    # Проверяем, заданы ли параметры для крестовины
    if (flow_o2 is None) and (v_o2 is None) and (angle_o2 is None):
        # Расчет для тройника
        result = (
            flow_o1 / flow_c * v_o1 * (math.cos(math.radians(angle_o1))) + flow_p / flow_c * v_p
        )
    else:
        # Расчет для крестовины
        result = (
            flow_o1 / flow_c * v_o1 * (math.cos(math.radians(angle_o1)))
            + flow_o2 / flow_c * v_o2 * (math.cos(math.radians(angle_o2)))
            + flow_p / flow_c * v_p
        )
    return result


# Расчет тройника на разделение (функция от угла)
def dzeta_diverge(alfa, v_current, v_c):
    """
    Рассчитывает КМС для одного "пути" в тройнике или крестовине при движении среды на РАЗДЕЛЕНИЕ.
    По: Щекин, Кореневский «Справочник по теплоснабжению и вентиляции (изд. 4-е)», 1976,
    стр. 97 (формула 51).

    Возвращает коэффициент местного сопротивления.
    """
    if v_c * math.cos(math.radians(alfa)) > v_current:
        result = (
            math.sin(math.radians(alfa)) ** 2
            + (math.cos(math.radians(alfa)) - v_current / v_c) ** 2
        )
        print("math.sin(math.radians(alfa)):", math.sin(math.radians(alfa)))
        print("math.cos(math.radians(alfa)):", math.cos(math.radians(alfa)))
        print("v_current / v_c:", v_current / v_c)

        print("v:", v_current, "v_c:", v_c)
    else:
        result = (
            math.sin(math.radians(alfa)) ** 2
            + 0.5 * (1 - v_c * math.cos(math.radians(alfa)) / v_current) * (v_current / v_c) ** 2
        )
    return result


def dzeta_converge(v_current, v_c, v_base):
    """
    Рассчитывает КМС для одного "пути" в тройнике или крестовине при движении среды на СМЕШЕНИЕ.
    По: Щекин, Кореневский «Справочник по теплоснабжению и вентиляции (изд. 4-е)», 1976,
    стр. 98 (формула 55).

    Возвращает коэффициент местного сопротивления.
    """

    if v_base > v_c:
        result = ((v_current / v_c) ** 2 - (v_base / v_c) ** 2) + (v_base / v_c - 1) ** 2
    else:
        result = ((v_current / v_c) ** 2 - (v_base / v_c) ** 2) + 0.5 * (1 - v_base / v_c)
    return result


def tee(
    temperature,
    angle,
    flowtype,
    flow_c=None,
    flow_o=None,
    flow_p=None,
    diameter_c=None,
    height_c=None,
    width_c=None,
    diameter_o=None,
    height_o=None,
    width_o=None,
    diameter_p=None,
    height_p=None,
    width_p=None,
    thermophysics="idelchik",
):
    """
    Рассчитывает потери давления в тройнике.
    По: Щекин, Кореневский «Справочник по теплоснабжению и вентиляции (изд. 4-е)», 1976,
    стр. 97 (формула 51).
    Индекс «c» относится к смесительному патрубку (магистральный патрубок с суммарным расходом).
    Индекс «o» относится к ответвлению (немагистральный патрубок).
    Индекс «p» («п») относится к проходу (магистральный патрубок с частичным расходом).
    По каждому патрубку нужно задать пару height/width или diameter.
    Требуется задать два из трех расходов v.

    Аргументы:
    temperature - температура воздуха, °C
    angle - угол между ответвлением и проходом, °
    flowtype - одно из двух
        "converge" (смешение, вытяжная система)
        "diverge" (разделение, приточная система)
    flow_x - расход воздуха, куб.м/ч
    diameter_x - диаметр патрубка, м
    height_x - высота патрубка, м
    width_x - ширина патрубка, м
    thermophysics - модель термофизических свойств (idelchik или thermo)

    Возвращает:
    Словарь с потерями давления на трение, Па.
    Ключи словаря:
    'dP_o' - потери при движении среды «на отвод»,
    'dP_p' - потери при движении среды «на проход».
    """

    print("================================")
    print(
        f"""Расчет тройника с параметрами:
temperature: {temperature} °C, angle: {angle} м^3/ч, flowtype: {flowtype}, thermophysics: {thermophysics},
flow_c: {flow_c} куб.м/ч, flow_o: {flow_o} куб.м/ч, flow_p: {flow_p} куб.м/ч,
height_c: {height_c} м, width_c: {width_c} м, diameter_c: {diameter_c} м,
height_o: {height_o} м, width_o: {width_o} м, diameter_o: {diameter_o} м,
height_p: {height_p} м, width_p: {width_p} м, diameter_p: {diameter_p} м"""
    )

    ###########Проверки#############
    # Проверка, что задано два из трех расходов тройника
    assert (
        len(list(filter(None, [flow_c, flow_o, flow_p]))) == 2
    ), "Точно два из трех (flow_c, flow_o, flow_p) должны быть заданы."

    # Проверка, что задана либо оба из пары height/width, либо диаметр
    def validate_geometry(height, width, diameter, name):
        assert not (
            (height or width) and diameter
        ), f"Необходимо указать одно из двух: пару height_{name}/width_{name} или diameter_{name}."
        assert not (
            ((height is None) or (width is None)) and (diameter is None)
        ), f"Не указана ни пара height_{name}/width_{name}, ни diameter_{name}."
        assert (
            height and width
        ) or diameter, f"Неправильно указаны геометрические характеристики для {name}."

    # Проверка для каждой тройки параметров
    validate_geometry(height_c, width_c, diameter_c, "c")
    validate_geometry(height_o, width_o, diameter_o, "o")
    validate_geometry(height_p, width_p, diameter_p, "p")

    # Проверка, что flowtype имеет одно из двух допустимых значений
    assert flowtype in [
        "converge",
        "diverge",
    ], "flowtype должен быть одним из двух допустимых значений: converge или diverge."
    ###########Проверки#############

    # Получаем термофизические данные
    if thermophysics == "idelchik":
        density = density_mendeleev
    elif thermophysics == "thermo":
        density = density_thermo
    else:
        raise ValueError("Неизвестный вид термофизических данных")

    if flow_c is None:
        flow_c = flow_o + flow_p
        print(f"Рассчитано flow_c: {flow_c:.0f} куб.м/ч")
    elif flow_o is None:
        flow_o = flow_c - flow_p
        print(f"Рассчитано flow_o: {flow_o:.0f} куб.м/ч")
    elif flow_p is None:
        flow_p = flow_c - flow_o
        print(f"Рассчитано flow_p: {flow_p:.0f} куб.м/ч")

    # Расчет скоростей
    print("v_c: ", end="")
    v_c = velocity(flow_c, height_c, width_c, diameter_c)
    print("v_o:", end="")
    v_o = velocity(flow_o, height_o, width_o, diameter_o)
    print("v_p:", end="")
    v_p = velocity(flow_p, height_p, width_p, diameter_p)

    # Расчет коэффициентов сопротивления
    if flowtype == "converge":
        # Расчет для тройника на смешение
        # Расчет наивыгоднейшей скорости смешения для конкретного патрубка (v_base)
        v_base = velocity_best_mixture(
            flow_o1=flow_o,
            v_o1=v_o,
            angle_o1=angle,
            flow_o2=None,
            v_o2=None,
            angle_o2=None,
            flow_p=flow_p,
            v_p=v_p,
            flow_c=flow_c,
        )
        print(f"Рассчитана наивыг. скорость смешения v_base: {v_base:.3f}")
        dzeta_o = dzeta_converge(v_current=v_o, v_c=v_c, v_base=v_base)
        dzeta_p = dzeta_converge(v_current=v_p, v_c=v_c, v_base=v_base)
    elif flowtype == "diverge":
        # Расчет для тройника на разделение. При проходе угол = 0
        dzeta_o = dzeta_diverge(alfa=angle, v_current=v_o, v_c=v_c)
        dzeta_p = dzeta_diverge(alfa=0, v_current=v_p, v_c=v_c)

    print(f"КМС тройника на отвод: {dzeta_o:.3f}")
    print(f"КМС тройника на проход: {dzeta_p:.3f}")

    # Расчет динамического давления по скорости v_c
    p_dyn = dynamic_pressure(density(temperature), v_c)

    # Расчет потерь давления "на отвод"
    dP_o = p_dyn * dzeta_o
    # Расчет потерь давления "на проход"
    dP_p = p_dyn * dzeta_p

    result = {
        "dP_p": dP_p,
        "dP_o": dP_o,
    }

    print(f"Полные dP тройника, на отвод: {result['dP_o']:.3f} Па")
    print(f"Полные dP тройника, на проход: {result['dP_p']:.3f} Па")
    print("================================")

    return result

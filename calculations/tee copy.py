import math
from physics.hydraulic import (
    reynolds_number,
    friction_factor,
    velocity,
    dynamic_pressure,
    hydraulic_diameter,
)
from physics.thermophysical import (
    kinematic_viscosity_idelchik,
    kinematic_viscosity_thermo,
    density_mendeleev,
    density_thermo,
)


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
    roughness=0.001,
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
    height_x - высота патрубка, м
    width_x - ширина патрубка, м
    diameter_x - диаметр патрубка, м
    v_x - расход воздуха, куб.м/ч
    roughness - абсолютная шероховатость, м
    thermophysics - модель термофизических свойств (idelchik или thermo)

    Возвращает:
    Потери давления на трение, Па
    """

    print("================================")
    print(
        f"""Расчет тройника с параметрами:
temperature: {temperature} °C, angle: {angle} м^3/ч, flowtype: {flowtype},
roughness: {roughness} °C, thermophysics: {thermophysics},
flow_c: {flow_c} куб.м/ч, flow_o: {flow_o} куб.м/ч, flow_p: {flow_p} куб.м/ч,
height_c: {height_c} м, width_c: {width_c} м, diameter_c: {diameter_c} м,
height_o: {height_o} м, width_o: {width_o} м, diameter_o: {diameter_o} м,
height_p: {height_p} м, width_p: {width_p} м, diameter_p: {diameter_p} м"""
    )

    ###########Проверки#############
    # Проверка, что задано два из трех расходов тройника
    assert (
        (flow_c is not None and flow_o is not None and flow_p is None)
        or (flow_c is None and flow_o is not None and flow_p is not None)
        or (flow_c is not None and flow_o is None and flow_p is not None)
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
        # Расчет наивыгоднейшей скорости смешения
        v_base_c = flow_o / flow_c * v_o * (math.cos(math.radians(angle))) + flow_p / flow_c * v_p
        print(f"Рассчитана наивыг. скорость смешения v_base_c: {v_base_c:.3f}")
        if v_base_c > v_c:
            dzeta_o = math.sin(math.radians(angle)) ** 2
            dzeta_p = ((v_o / v_c) ** 2 - (v_base_c / v_c) ** 2) + (v_base_c / v_c - 1) ** 2
        else:
            dzeta_o = ((v_o / v_c) ** 2 - (v_base_c / v_c) ** 2) + 0.5 * (1 - v_base_c / v_c)
            dzeta_p = ((v_p / v_c) ** 2 - (v_base_c / v_c) ** 2) + 0.5 * (1 - v_base_c / v_c)
    elif flowtype == "diverge":

        # Расчет тройника на разделение (функция от угла и скорости патрубка, для которого считаем dzeta)
        def dzeta_diverge(alfa, v_current):
            if v_c * math.cos(math.radians(alfa)) > v_o:
                result = (
                    math.sin(math.radians(alfa)) ** 2
                    + (math.cos(math.radians(alfa)) - v_current / v_c) ** 2
                )
            else:
                result = (
                    math.sin(math.radians(alfa)) ** 2
                    + 0.5
                    * (1 - v_c * math.cos(math.radians(alfa)) / v_current)
                    * (v_current / v_c) ** 2
                )
            return result

        # Расчет для тройника на разделение при проходе угол = 0
        dzeta_o = dzeta_diverge(alfa=angle, v_current=v_o)
        dzeta_p = dzeta_diverge(alfa=0, v_current=v_p)

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

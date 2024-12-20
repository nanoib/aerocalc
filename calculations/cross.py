import math
from physics.hydraulic import (
    velocity,
    dynamic_pressure,
)
from physics.thermophysical import (
    density_mendeleev,
    density_thermo,
)

from calculations.tee import velocity_best_mixture, dzeta_converge, dzeta_diverge


def cross(
    temperature,
    flowtype,
    flow_c=None,
    flow_o1=None,
    flow_o2=None,
    flow_p=None,
    diameter_c=None,
    height_c=None,
    width_c=None,
    angle_o1=None,
    diameter_o1=None,
    height_o1=None,
    width_o1=None,
    angle_o2=None,
    diameter_o2=None,
    height_o2=None,
    width_o2=None,
    diameter_p=None,
    height_p=None,
    width_p=None,
    roughness=0.001,
    thermophysics="idelchik",
):
    """
    Рассчитывает потери давления в крестовине на основе функции для расчета потерь в тройнике.
    По: Щекин, Кореневский «Справочник по теплоснабжению и вентиляции (изд. 4-е)», 1976,
    стр. 98 (пункт 53).
    Рассчитываются как тройники.
    Индекс «c» относится к смесительному патрубку (магистральный патрубок с суммарным расходом).
    Индексы «o1» и «o2» относится к ответвлениям (немагистральные патрубки).
    Индекс «p» (типа вметсо кириллической «п») относится к проходу (т.е. это магистральный
    патрубок с частичным расходом).
    По каждому патрубку нужно задать пару height/width или diameter.
    Требуется задать три из четырех расходов flow_x.

    Аргументы:
    temperature - температура воздуха, °C
    angle - угол между ответвлением и проходом, °
    flowtype - вариант движения среды, одно из двух
        "converge" (смешение, вытяжная система)
        "diverge" (разделение, приточная система)
    flow_x - расход воздуха, куб.м/ч
    height_x - высота патрубка, м
    width_x - ширина патрубка, м
    diameter_x - диаметр патрубка, м
    thermophysics - модель термофизических свойств (idelchik или thermo)

    Возвращает:
    Словарь с потерями давления на трение, Па.
    Ключи словаря:
    'dP_o' - потери при движении среды «на отвод»,
    'dP_p' - потери при движении среды «на проход».
    """

    print("================================")
    print(
        f"""Расчет тройника/крестовины с параметрами:
temperature: {temperature} °C, flowtype: {flowtype},
roughness: {roughness} °C, thermophysics: {thermophysics},
flow_c: {flow_c} куб.м/ч, flow_o: {flow_o1} куб.м/ч, flow_o: {flow_o2} куб.м/ч, flow_p: {flow_p} куб.м/ч,
height_c: {height_c} м, width_c: {width_c} м, diameter_c: {diameter_c} м,
height_o1: {height_o1} м, width_o1: {width_o1} м, diameter_o1: {diameter_o1} м, angle_o1: {angle_o1} м^3/ч,
height_o2: {height_o2} м, width_o2: {width_o2} м, diameter_o2: {diameter_o2} м, angle_o2: {angle_o2} м^3/ч,
height_p: {height_p} м, width_p: {width_p} м, diameter_p: {diameter_p} м"""
    )

    flows = [flow_c, flow_o1, flow_o2, flow_p]

    ###########Проверки#############
    # Проверка, что задано три из четырех расходов тройника
    assert (
        len(list(filter(None, flows))) == 3
    ), "Точно три из четырех (flow_c, flow_o1, flow_o2, flow_p) должны быть заданы."

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
    validate_geometry(height_o1, width_o1, diameter_o1, "o")
    validate_geometry(height_o2, width_o2, diameter_o2, "o")
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
        flow_c = sum(list(filter(None, flows)))
        print(f"Рассчитано flow_c: {flow_c:.0f} куб.м/ч")
    elif flow_o1 is None:
        flow_o1 = flow_c - flow_o2 - flow_p
        print(f"Рассчитано flow_o1: {flow_o1:.0f} куб.м/ч")
    elif flow_o2 is None:
        flow_o2 = flow_c - flow_o1 - flow_p
        print(f"Рассчитано flow_o1: {flow_o2:.0f} куб.м/ч")
    elif flow_p is None:
        flow_p = flow_c - flow_o1 - flow_o2 - flow_p
        print(f"Рассчитано flow_p: {flow_p:.0f} куб.м/ч")

    assert flow_c == flow_o1 + flow_o2 + flow_p, "Расходы заданы не верно"

    # Расчет скоростей
    print("v_c: ", end="")
    v_c = velocity(flow_c, height_c, width_c, diameter_c)
    print("v_o1:", end="")
    v_o1 = velocity(flow_o1, height_o1, width_o1, diameter_o1)
    print("v_o2:", end="")
    v_o2 = velocity(flow_o2, height_o2, width_o2, diameter_o2)
    print("v_p:", end="")
    v_p = velocity(flow_p, height_p, width_p, diameter_p)

    # Расчет коэффициентов сопротивления
    if flowtype == "converge":
        # Расчет для тройника на смешение
        # Расчет наивыгоднейшей скорости смешения для конкретного патрубка (v_base)
        v_base = velocity_best_mixture(
            flow_o1=flow_o1,
            v_o1=v_o1,
            angle_o1=angle_o1,
            flow_o2=flow_o2,
            v_o2=v_o2,
            angle_o2=angle_o2,
            flow_p=flow_p,
            v_p=v_p,
            flow_c=flow_c,
        )
        print(f"Рассчитана наивыг. скорость смешения v_base: {v_base:.3f}")
        dzeta_o1 = dzeta_converge(v_current=v_o1, v_c=v_c)
        dzeta_o2 = dzeta_converge(v_current=v_o2, v_c=v_c)
        dzeta_p = dzeta_converge(v_current=v_p, v_c=v_c)
    elif flowtype == "diverge":
        # Расчет для тройника на разделение. При проходе угол = 0
        dzeta_o1 = dzeta_diverge(alfa=angle_o1, v_current=v_o1, v_c=v_c)
        dzeta_o2 = dzeta_diverge(alfa=angle_o2, v_current=v_o2, v_c=v_c)
        dzeta_p = dzeta_diverge(alfa=0, v_current=v_p, v_c=v_c)

    print(f"КМС тройника на отвод 1: {dzeta_o1:.3f}")
    print(f"КМС тройника на отвод 2: {dzeta_o2:.3f}")
    print(f"КМС тройника на проход: {dzeta_p:.3f}")

    # Расчет динамического давления по скорости v_c
    p_dyn = dynamic_pressure(density(temperature), v_c)

    # Расчет потерь давления "на отвод", патрубок 1
    dP_o1 = p_dyn * dzeta_o1
    # Расчет потерь давления "на отвод", патрубок 2
    dP_o2 = p_dyn * dzeta_o2
    # Расчет потерь давления "на проход"
    dP_p = p_dyn * dzeta_p

    result = {
        "dP_p": dP_p,
        "dP_o1": dP_o1,
        "dP_o1": dP_o2,
    }

    print(f"Полные dP крестовины, на отвод 1: {result['dP_o1']:.3f} Па")
    print(f"Полные dP крестовины, на отвод 2: {result['dP_o2']:.3f} Па")
    print(f"Полные dP крестовины, на проход: {result['dP_p']:.3f} Па")
    print("================================")

    return result

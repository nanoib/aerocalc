import unittest
from calculations.cross import cross


class TestCross(unittest.TestCase):
    def test_cross_pressure_loss_diverge_idelchik(self):
        """
        Проверка расчета. Исходные данные по примеру из файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx
        «Расчет тройника для приточной системы»
        Данные по Идельчик.
        Равные расходы по всем патрубкам.
        """
        result = cross(
            temperature=0,
            flowtype="diverge",
            flow_c=900,
            flow_o1=300,
            flow_o2=300,
            flow_p=None,
            diameter_c=0.160,
            diameter_o1=0.160,
            angle_o1=90,
            angle_o2=90,
            diameter_o2=0.160,
            diameter_p=0.160,
            thermophysics="idelchik",
        )

        # Значение ниже сравнивается со значением, полученным здесь же при первом запуске
        self.assertAlmostEqual(result["dP_p"], 44.423, places=2)
        self.assertAlmostEqual(result["dP_o1"], 105.506, places=2)
        self.assertAlmostEqual(result["dP_o2"], 105.506, places=2)

    def test_cross_pressure_loss_converge_idelchik(self):
        """
        То же, что выше, но converge
        """
        result = cross(
            temperature=0,
            flowtype="converge",
            flow_c=900,
            flow_o1=300,
            flow_o2=300,
            flow_p=None,
            diameter_c=0.160,
            diameter_o1=0.160,
            angle_o1=90,
            angle_o2=90,
            diameter_o2=0.160,
            diameter_p=0.160,
            thermophysics="idelchik",
        )

        # Значение ниже сравнивается со значением, полученным здесь же при первом запуске
        self.assertAlmostEqual(result["dP_p"], 54.295, places=2)
        self.assertAlmostEqual(result["dP_o1"], 54.295, places=2)
        self.assertAlmostEqual(result["dP_o2"], 54.295, places=2)

    def test_cross_pressure_loss_diverge_thermo(self):
        """
        То же, что выше, но thermo
        """
        result = cross(
            temperature=0,
            flowtype="diverge",
            flow_c=900,
            flow_o1=300,
            flow_o2=300,
            flow_p=None,
            diameter_c=0.160,
            diameter_o1=0.160,
            angle_o1=90,
            angle_o2=90,
            diameter_o2=0.160,
            diameter_p=0.160,
            thermophysics="thermo",
        )

        # Значение ниже сравнивается со значением, полученным здесь же при первом запуске
        self.assertAlmostEqual(result["dP_p"], 44.423, places=1)
        self.assertAlmostEqual(result["dP_o1"], 105.506, places=0)
        self.assertAlmostEqual(result["dP_o2"], 105.506, places=0)

    def test_cross_pressure_loss_square_converge_idelchik(self):
        """
        То же, что выше, но converge
        """
        result = cross(
            temperature=0,
            flowtype="diverge",
            flow_c=900,
            flow_o1=300,
            flow_o2=300,
            flow_p=None,
            height_c=0.2,
            width_c=0.4,
            height_o1=0.2,
            width_o1=0.2,
            height_o2=0.2,
            width_o2=0.2,
            angle_o1=60,
            angle_o2=60,
            diameter_p=0.160,
            thermophysics="idelchik",
        )

        # Значение ниже сравнивается со значением, полученным здесь же при первом запуске
        self.assertAlmostEqual(result["dP_p"], 1.366, places=2)
        self.assertAlmostEqual(result["dP_o1"], 5.086, places=2)
        self.assertAlmostEqual(result["dP_o2"], 5.086, places=2)

    def test_cross_assert(self):
        """
        Проверка выдачи assert если не задал, например, width_o1
        """
        with self.assertRaises(AssertionError):
            result = cross(
                temperature=0,
                flowtype="diverge",
                flow_c=900,
                flow_o1=300,
                flow_o2=300,
                flow_p=None,
                height_c=0.2,
                width_c=0.4,
                height_o1=0.2,
                height_o2=0.2,
                width_o2=0.2,
                angle_o1=60,
                angle_o2=60,
                diameter_p=0.160,
                thermophysics="idelchik",
            )

    def test_cross_square_round(self):
        """
        Вариант, когда магистраль прямоугольная, а отводы круглые.
        А еще задано все, кроме flow_o2
        """
        result = cross(
            temperature=0,
            flowtype="diverge",
            flow_c=900,
            flow_o1=300,
            flow_p=300,
            height_c=0.2,
            width_c=0.4,
            diameter_o1=0.160,
            angle_o1=90,
            angle_o2=90,
            diameter_o2=0.160,
            diameter_p=0.160,
            thermophysics="idelchik",
        )

        # Значение ниже сравнивается со значением, полученным здесь же при первом запуске
        self.assertAlmostEqual(result["dP_p"], 1.366, places=2)
        self.assertAlmostEqual(result["dP_o1"], 11.866, places=2)
        self.assertAlmostEqual(result["dP_o2"], 11.866, places=2)


if __name__ == "__main__":
    unittest.main()

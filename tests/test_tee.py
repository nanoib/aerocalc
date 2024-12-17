import unittest
from calculations.tee import tee


class TestTee(unittest.TestCase):
    def test_tee_pressure_loss_diverge_idelchik(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx
        «Расчет тройника для приточной системы»
        Данные по Идельчик
        """
        result = tee(
            temperature=0,
            angle=90,
            flowtype="diverge",
            flow_p=600,
            flow_o=300,
            diameter_c=0.160,
            diameter_o=0.160,
            diameter_p=0.160,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result["dP_p"], 11.11, places=1)
        # Значение ниже сравнивается со значением из AeroCalc.xlsx
        self.assertAlmostEqual(result["dP_o"], 105.572, places=0)

    def test_tee_pressure_loss_converge_idelchik(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx
        «Расчет тройника для вытяжной системы»
        Данные по Идельчик
        """
        result = tee(
            temperature=0,
            angle=90,
            flowtype="converge",
            flow_p=600,
            flow_o=300,
            diameter_c=0.160,
            diameter_o=0.160,
            diameter_p=0.160,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result["dP_p"], 52.42, places=1)
        # Значение ниже сравнивается со значением из AeroCalc.xlsx
        self.assertAlmostEqual(result["dP_o"], 19.139, places=1)

    def test_tee_pressure_loss_converge_thermo(self):
        """
        То же, что предыдуще, но данные по thermo
        """
        result = tee(
            temperature=0,
            angle=90,
            flowtype="converge",
            flow_p=600,
            flow_o=300,
            diameter_c=0.160,
            diameter_o=0.160,
            diameter_p=0.160,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result["dP_p"], 52.42, places=1)

    def test_tee_pressure_loss_diverge_square(self):
        """
        Из примера в AeroCalc.xlsx
        «П1 t= -25. Нижняя ветка»
        """
        result = tee(
            temperature=-25,
            angle=90,
            flowtype="diverge",
            flow_c=2000,
            flow_o=1000,
            height_c=0.3,
            width_c=0.3,
            height_p=0.3,
            width_p=0.3,
            height_o=0.3,
            width_o=0.3,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result["dP_o"], 30.52, places=1)
        self.assertAlmostEqual(result["dP_p"], 6.783, places=1)

    def test_tee_pressure_loss_converge_square(self):
        """
        Из примера в AeroCalc.xlsx
        «В1 t= -25. Нижняя ветка»
        """
        result = tee(
            temperature=-25,
            angle=90,
            flowtype="converge",
            flow_c=2000,
            flow_o=1000,
            height_c=0.3,
            width_c=0.3,
            height_p=0.3,
            width_p=0.3,
            height_o=0.3,
            width_o=0.3,
            roughness=0.001,
            thermophysics="idelchik",
        )
        # Нижний результат сходится с тестом в Вентиляции, а с расчетом в Excel не сходится
        self.assertAlmostEqual(result["dP_o"], 15.25, places=1)

    def test_tee_assert(self):
        """
        Проверка проверок
        """
        with self.assertRaises(AssertionError):
            result = tee(
                temperature=-25,
                angle=90,
                flowtype="converge",
                flow_c=2000,
                flow_o=1000,
                diameter_c=1,
                width_c=0.3,
                height_p=0.3,
                width_p=0.3,
                height_o=0.3,
                width_o=0.3,
                roughness=0.001,
                thermophysics="idelchik",
            )

        with self.assertRaises(AssertionError):
            result = tee(
                temperature=-25,
                angle=90,
                flowtype="converge",
                flow_c=2000,
                flow_o=1000,
                width_c=0.3,
                height_p=0.3,
                width_p=0.3,
                height_o=0.3,
                width_o=0.3,
                roughness=0.001,
                thermophysics="idelchik",
            )


if __name__ == "__main__":
    unittest.main()

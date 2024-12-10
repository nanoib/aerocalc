import unittest
from calculations.duct import duct


class TestDuct(unittest.TestCase):
    def test_pressure_loss_idelchik(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx
        Данные по Идельчик
        """
        result = duct(
            flow=600,
            length=1.37,
            temperature=0,
            diameter=0.16,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 12.06, places=1)

    def test_pressure_loss_thermo(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx
        Данные по thermo
        """
        result = duct(
            flow=600,
            length=1.37,
            temperature=0,
            diameter=0.16,
            roughness=0.001,
            thermophysics="thermo",
        )
        self.assertAlmostEqual(result, 12.06, places=1)

    def test_assert_errors(self):
        with self.assertRaises(AssertionError):
            """Проверка выдачи assert если не указана ширина воздуховода"""
            duct(flow=600, length=1.37, temperature=0, height=0.3)
        with self.assertRaises(AssertionError):
            """Проверка выдачи assert если не указаны никакие габариты"""
            duct(flow=600, length=1.37, temperature=0)
        with self.assertRaises(AssertionError):
            """Проверка выдачи assert если указан только диаметр и высота"""
            duct(flow=600, length=1.37, temperature=0, diameter=0.16, height=0.3)


if __name__ == "__main__":
    unittest.main()

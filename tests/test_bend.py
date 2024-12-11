import unittest
from calculations.elbow import elbow


class Testelbow(unittest.TestCase):
    def test_elbow_pressure_loss_idelchik(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx, данные по Идельчик.
        Учитываются параметры kdelta и kre,
        а также учет реального соотношения a0/bo, которые (возможно) не
        учитываются на момент версии 24.1.
        """
        result = elbow(
            flow=600,
            temperature=0,
            angle=90,
            r0=0.185,
            diameter=0.16,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 25.116, places=1)

    def test_elbow_pressure_loss_idelchik_22(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx, данные по Идельчик.
        k_delta и k_re приняты 1.
        """
        result = elbow(
            flow=600,
            temperature=0,
            angle=90,
            r0=0.185,
            diameter=0.16,
            roughness=0.001,
            thermophysics="idelchik",
            calcversion="22",
        )
        self.assertAlmostEqual(result, 11.27, places=1)

    def test_elbow_pressure_loss_square(self):
        """
        Проверка примера из AeroCalc.xlsx (квадратный) без учета kdelta, kre
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.3,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="vert",
            roughness=0.001,
            thermophysics="idelchik",
            calcversion="22",
        )
        self.assertAlmostEqual(result, 2.45, places=1)

    def test_elbow_pressure_loss_square(self):
        """
        Проверка примера из AeroCalc.xlsx (квадратный)
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.3,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="vert",
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 6.195, places=1)

    def test_elbow_pressure_loss_horiz(self):
        """
        Проверка примера из AeroCalc.xlsx (проверка, что vert-horiz для квадратных не влияет)
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.3,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="horiz",
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 6.195, places=1)

    def test_elbow_pressure_loss_square_delta(self):
        """
        Проверка примера из AeroCalc.xlsx с шероховатостью 0.0001
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.3,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="vert",
            roughness=0.0001,
            thermophysics="idelchik",
            calcversion="22",
        )
        self.assertAlmostEqual(result, 2.372, places=2)

    def test_elbow_pressure_loss_a0b0(self):
        """
        Проверка примера из AeroCalc.xlsx (проверка, что a0b0 и ориентация влияют #1 гориз)
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.6,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="horiz",
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 10.355, places=1)

    def test_elbow_pressure_loss_a0b0(self):
        """
        Проверка примера из AeroCalc.xlsx (проверка, что a0b0 и ориентация влияют #2 вертик.)
        """
        result = elbow(
            flow=1000,
            height=0.3,
            width=0.6,
            temperature=-25,
            angle=90,
            r0=0.25,
            oriented="vert",
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 1.557, places=1)

    def test_elbow_pressure_loss_assert(self):
        """
        Проверка выдачи assert если задать много габаритов.
        """
        with self.assertRaises(AssertionError):
            result = elbow(
                flow=1000,
                height=0.3,
                width=0.6,
                diameter=0.125,
                temperature=-25,
                angle=90,
                r0=0.25,
                oriented="vert",
                roughness=0.001,
                thermophysics="idelchik",
            )

    def test_elbow_pressure_loss_thermo(self):
        """
        Проверка работы при взятии термофизических параметров из thermo.
        """
        with self.assertRaises(AssertionError):
            result = elbow(
                flow=1000,
                height=0.3,
                width=0.6,
                diameter=0.125,
                temperature=-25,
                angle=90,
                r0=0.25,
                oriented="vert",
                roughness=0.001,
                thermophysics="thermo",
            )


if __name__ == "__main__":
    unittest.main()

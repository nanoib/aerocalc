import unittest
from calculations.transition import transition


class Testtransition(unittest.TestCase):
    def test_transition_diffusor_pressure_loss_idelchik(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx, данные по Идельчик.
        Расчет на расширение.
        В версии 24.1 скорость считается по большему сечению, что неверно.
        """
        result = transition(
            flow=300,
            temperature=0,
            diameter1=0.125,
            height1=None,
            width1=None,
            diameter2=0.16,
            height2=None,
            width2=None,
            length=0.078,
            roughness=0.0015,
            thermophysics="idelchik",
            calcversion="22",
        )
        self.assertAlmostEqual(result, 0.986, places=2)

    def test_transition_diffusor_pressure_loss_thermo(self):
        """
        То же, что выше, но с расчетом по thermo
        """
        result = transition(
            flow=300,
            temperature=0,
            diameter1=0.125,
            height1=None,
            width1=None,
            diameter2=0.16,
            height2=None,
            width2=None,
            length=0.078,
            roughness=0.0015,
            thermophysics="thermo",
            calcversion="22",
        )
        self.assertAlmostEqual(result, 0.986, places=2)

    def test_transition_diffusor_pressure_loss_square(self):
        """
        Расчет из AeroCalc.xslx
        """
        result = transition(
            flow=2000,
            temperature=-25,
            diameter1=None,
            height1=0.3,
            width1=0.3,
            diameter2=None,
            height2=0.6,
            width2=0.6,
            length=0.22,
            roughness=0.001,
            thermophysics="idelchik",
        )
        self.assertAlmostEqual(result, 30.413, places=1)

    def test_transition_confusor_pressure_loss_square(self):
        """
        Проверка примера из исходного файла с формулами аэрод. расчета
        Расчеты в nanoCAD BIM Вентиляция.docx, данные по Идельчик.
        Расчет на сужение.
        """
        result = transition(
            flow=300,
            temperature=0,
            diameter1=0.16,
            height1=None,
            width1=None,
            diameter2=0.125,
            height2=None,
            width2=None,
            length=0.078,
            roughness=0.0015,
            thermophysics="idelchik",
            # calcversion="22",
        )
        self.assertAlmostEqual(result, 0.4, places=1)


if __name__ == "__main__":
    unittest.main()

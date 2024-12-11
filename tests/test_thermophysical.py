import unittest
from physics.thermophysical import (
    kinematic_viscosity_idelchik,
    kinematic_viscosity_thermo,
    density_mendeleev,
    density_thermo,
)


class TestThermophysical(unittest.TestCase):
    def test_kinematic_viscosity_thermo(self):
        """
        Проверка значения кинематической вязкости по thermo
        """
        result = kinematic_viscosity_thermo(t=0)
        self.assertAlmostEqual(result, 1.32e-5, places=2)

    def test_kinematic_viscosity_idelchik(self):
        """
        Проверка значения кинематической вязкости по Идельчик
        """
        result = kinematic_viscosity_thermo(t=0)
        self.assertAlmostEqual(result, 1.32e-5, places=2)

    def test_density_thermo(self):
        """
        Проверка значения плотности по thermo
        """
        result = density_thermo(t=0)
        self.assertAlmostEqual(result, 1.294, places=2)

    def test_density_mendeleev(self):
        """
        Проверка значения плотности по Менделееву
        """
        result = density_mendeleev(t=0)
        self.assertAlmostEqual(result, 1.294, places=2)

    def test_nu_extra_up(self):
        """
        Проверка значения плотности по Менделееву
        (экстраполяция вверх)
        """
        t = 850
        result = kinematic_viscosity_idelchik(t)
        self.assertAlmostEqual(result, kinematic_viscosity_thermo(t), places=2)

    def test_nu_extra_down(self):
        """
        Проверка значения плотности по Менделееву
        (экстраполяция вниз)
        """
        t = -41
        result = kinematic_viscosity_idelchik(t)
        self.assertAlmostEqual(result, kinematic_viscosity_thermo(t), places=2)

    def test_nu_extra_down_assert(self):
        """
        Проверка, что срабатывает предел экстраполяции
        (экстраполяция вниз)
        """
        t = -81
        with self.assertRaises(AssertionError):
            kinematic_viscosity_idelchik(t)


if __name__ == "__main__":
    unittest.main()

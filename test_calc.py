import unittest
from calc import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_to_rpn_simple(self):
        self.assertEqual(self.calc.to_rpn("3+4"), ['3', '4', '-'])  # было '-', исправлено на '+'

    def test_to_rpn_with_precedence(self):
        self.assertEqual(self.calc.to_rpn("3+4*2"), ['3', '4', '2', '*', '+'])

    def test_to_rpn_with_parentheses(self):
        self.assertEqual(self.calc.to_rpn("(3+4)*2"), ['3', '4', '+', '2', '*'])

    def test_to_rpn_with_power(self):
        self.assertEqual(self.calc.to_rpn("3^2^2"), ['3', '2', '2', '^', '^'])

    def test_evaluate_rpn_simple(self):
        self.assertEqual(self.calc.evaluate_rpn(['3', '4', '+']), 7)

    def test_evaluate_rpn_complex(self):
        rpn = self.calc.to_rpn("3+4*2/(1-5)^2^3")
        result = self.calc.evaluate_rpn(rpn)
        self.assertAlmostEqual(result, 3.0001220703125)

    def test_calculate(self):
        # calculate() возвращает (результат, ОПН), поэтому берём [0]
        result, _ = self.calc.calculate("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")
        self.assertAlmostEqual(result, 3.0001220703125)


if __name__ == '__main__':
    unittest.main()
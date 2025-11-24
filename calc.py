class Calculator:
    def __init__(self):
        # Приоритеты операций: +, - (1), *, / (2), ^ (3)
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(self, c):
        return c in '+-*/^'

    def to_rpn(self, expression):
        """Преобразование инфиксного выражения в обратную польскую нотацию"""
        stack = []
        output = []
        i = 0
        while i < len(expression):
            c = expression[i]
            if c.isdigit() or c == '.':
                # Считываем число с возможной десятичной точкой
                num = c
                while i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                    i += 1
                    num += expression[i]
                output.append(num)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Удаляем '('
            elif self.is_operator(c):
                while stack and stack[-1] != '(' and (
                    self.precedence[stack[-1]] > self.precedence[c] or
                    (self.precedence[stack[-1]] == self.precedence[c] and c != '^')
                ):
                    output.append(stack.pop())
                stack.append(c)
            i += 1
        while stack:
            output.append(stack.pop())
        return output

    def evaluate_rpn(self, rpn):
        """Вычисление выражения, записанного в обратной польской нотации"""
        stack = []
        for token in rpn:
            if token not in self.precedence:
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        return stack[0]

    def calculate(self, expression):
        """Вычисление результата выражения в инфиксной форме"""
        rpn = self.to_rpn(expression.replace(' ', ''))
        return self.evaluate_rpn(rpn)


# Пример использования
calc = Calculator()
expr = "3 + 4 * 2 / (1 - 5) ^ 2 ^ 3"
result = calc.calculate(expr)
print(result)  # Выведет около 3.0001220703125
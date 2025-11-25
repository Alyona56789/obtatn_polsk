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
                if stack:
                    stack.pop()  # Удаляем '('
                else:
                    raise ValueError("Несбалансированные скобки")
            elif self.is_operator(c):
                while stack and stack[-1] != '(' and (
                    self.precedence.get(stack[-1], 0) > self.precedence[c] or
                    (self.precedence.get(stack[-1], 0) == self.precedence[c] and c != '^')
                ):
                    output.append(stack.pop())
                stack.append(c)
            i += 1
        while stack:
            if stack[-1] in '()':
                raise ValueError("Несбалансированные скобки")
            output.append(stack.pop())
        return output

    def evaluate_rpn(self, rpn):
        """Вычисление выражения, записанного в обратной польской нотации"""
        stack = []
        for token in rpn:
            if token not in self.precedence:
                try:
                    stack.append(float(token))
                except ValueError:
                    raise ValueError(f"Некорректное число: {token}")
            else:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов для оператора")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]

    def calculate(self, expression):
        """Вычисление результата выражения в инфиксной форме"""
        expression = expression.replace(' ', '')
        if not expression:
            raise ValueError("Пустое выражение")
        rpn = self.to_rpn(expression)
        return self.evaluate_rpn(rpn)


# Ввод выражения с консоли
if __name__ == "__main__":
    calc = Calculator()
    try:
        expr = input("Введите математическое выражение: ")
        expr_clean = expr.replace(' ', '')
        if not expr_clean:
            raise ValueError("Пустое выражение")
        rpn = calc.to_rpn(expr_clean)
        print("Обратная польская запись:", ' '.join(rpn))
        result = calc.evaluate_rpn(rpn)
        print("Результат:", result)
    except Exception as e:
        print("Ошибка:", e)
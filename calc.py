import re

class Calculator:
    def __init__(self):
        # Приоритеты операций: +, - (1), *, / (2), ^ (3)
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_operator(self, c):
        return c in '+-*/^'

    def preprocess_implicit_multiplication(self, expr):
        """Добавляет пропущенные '*' для неявного умножения"""
        # Убираем пробелы
        expr = expr.replace(' ', '')
        # 1. Число перед открывающей скобкой: 5( → 5*(
        expr = re.sub(r'(\d)\(', r'\1*(', expr)
        # 2. Закрывающая скобка перед числом: )5 → )*5
        expr = re.sub(r'\)(\d)', r')*\1', expr)
        # 3. Закрывающая скобка перед открывающей: )( → )*(
        expr = re.sub(r'\)\(', r')*(', expr)
        return expr

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
        """Вычисление результата выражения в инфиксной форме с поддержкой неявного умножения"""
        if not expression:
            raise ValueError("Пустое выражение")
        expr_clean = self.preprocess_implicit_multiplication(expression)
        rpn = self.to_rpn(expr_clean)
        return self.evaluate_rpn(rpn), rpn  # Возвращаем и результат, и ОПН


# Ввод выражения с консоли
if __name__ == "__main__":
    calc = Calculator()
    try:
        expr = input("Введите математическое выражение: ")
        result, rpn = calc.calculate(expr)
        print("Обратная польская запись:", ' '.join(rpn))
        print("Результат:", result)
    except Exception as e:
        print("Ошибка:", e)
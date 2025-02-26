from __future__ import annotations

import re
from decimal import Decimal
from operator import add, mod, mul, pow, sub, truediv
from typing import Callable


class Symbol:
    pass


class Operator(Symbol):
    def __init__(self, op: Convertor, count=2, priority=1):
        self.op = op
        self.count = count
        self.priority = priority

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.op.__name__}, priority={self.priority})'

    def calc(self, *args: Decimal):
        if len(args) != self.count:
            raise ValueError
        return self.op(*args)

    __repr__ = __str__


class Bracket(Symbol):
    def __init__(self, pair: str | None = None, is_head=False):
        self.pair = pair
        self.is_head = is_head

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(pair={repr(self.pair)})'

    __repr__ = __str__


Convertor = Callable[..., Decimal]

symbols: dict[re.Pattern, Convertor | Operator | Bracket] = {
    re.compile(r'(?<!\d)(\+|-)?\d+(\.\d+)?'): Decimal,
    re.compile(r'\+'): Operator(add),
    re.compile(r'-'): Operator(sub),
    re.compile(r'\*'): Operator(mul, priority=2),
    re.compile(r'x'): Operator(mul, priority=2),
    re.compile(r'/'): Operator(truediv, priority=2),
    re.compile(r'÷'): Operator(truediv, priority=2),
    re.compile(r'%'): Operator(mod, priority=2),
    re.compile(r'mod'): Operator(mod, priority=2),
    re.compile(r'^'): Operator(pow, priority=3),
    re.compile(r'\('): Bracket('()', is_head=True),
    re.compile(r'\)'): Bracket('()'),
    re.compile(r'\['): Bracket('[]', is_head=True),
    re.compile(r'\]'): Bracket('[]'),
}


def parse_symbol(expression: str, pos: int):
    """解析表达式并返回解析后的结果"""
    for pattern, op in symbols.items():
        span = pattern.match(expression, pos=pos)
        if span is None:
            continue
        return op, span
    raise ValueError("不支持的符号 %r" % expression[pos])


def calc(expression: str) -> Decimal:
    return calc_preprocessed(preprocess(expression))


def preprocess(expression: str) -> list[Decimal | Operator]:
    stack: list[Operator | Bracket] = []
    preprocessed: list[Decimal | Operator] = []

    expression = expression.replace(' ', '')
    pos = 0
    while pos < len(expression):
        symbol, span = parse_symbol(expression, pos)
        if not isinstance(symbol, Symbol):
            preprocessed.append(symbol(expression[span.start():span.end()]))
        elif isinstance(symbol, Operator):
            while stack and isinstance(stack[-1], Operator) and stack[-1].priority >= symbol.priority:
                preprocessed.append(stack[-1])
                del stack[-1]
            stack.append(symbol)
        else:
            if symbol.is_head:
                stack.append(symbol)
            else:
                while isinstance(stack[-1], Operator):
                    preprocessed.append(stack[-1])
                    del stack[-1]
                if isinstance(stack[-1], Bracket) and stack[-1].pair != symbol.pair:
                    raise ValueError("不匹配的括号 %r" % symbol.pair)
                del stack[-1]
        pos = span.end()

    preprocessed.extend(reversed([i for i in stack if isinstance(i, Operator)]))
    return preprocessed


def calc_preprocessed(preprocessed: list[Decimal | Operator]):
    stack: list[Decimal] = []
    for sign in preprocessed:
        if isinstance(sign, Operator):
            if len(stack) < sign.count:
                raise ValueError("表达式错误")
            result = sign.calc(*stack[-sign.count:])
            stack = stack[:-sign.count]
            stack.append(result)
        else:
            stack.append(sign)

    if len(stack) != 1:
        raise ValueError("表达式错误")
    return stack[0]


def main():
    result = calc("1 + (6 + 2) * 3")
    print(result)


if __name__ == "__main__":
    main()

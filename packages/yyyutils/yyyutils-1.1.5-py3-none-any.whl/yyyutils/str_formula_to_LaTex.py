from typing import Dict, Optional, Union, List
import re
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    VARIABLE = "VARIABLE"
    FUNCTION = "FUNCTION"
    BRACKET = "BRACKET"
    DELIMITER = "DELIMITER"


@dataclass
class Token:
    type: TokenType
    value: str
    position: int


class LatexFormatError(Exception):
    """LaTeX格式转换错误"""
    pass


class FormulaParser:
    """数学公式解析器"""

    # LaTeX符号映射
    LATEX_SYMBOLS = {
        # 基础运算符
        '*': '\\times',
        '/': '\\div',
        '.': '\\cdot',
        # '^': '\\^',

        # 比较运算符
        '>=': '\\geq',
        '<=': '\\leq',
        '!=': '\\neq',
        '==': '=',
        '>': '>',
        '<': '<',

        # 数学函数
        'sum': '\\sum',
        'prod': '\\prod',
        'int': '\\int',
        'oint': '\\oint',
        'iint': '\\iint',
        'oiint': '\\oiint',
        'sqrt': '\\sqrt',
        'sin': '\\sin',
        'cos': '\\cos',
        'tan': '\\tan',
        'log': '\\log',
        'ln': '\\ln',
        'lim': '\\lim',

        # 其他数学符号
        'inf': '\\infty',
        'alpha': '\\alpha',
        'beta': '\\beta',
        'gamma': '\\gamma',
        'delta': '\\delta',
        'theta': '\\theta',
        'pi': '\\pi',
        'sigma': '\\sigma',
        'omega': '\\omega'
    }

    # 运算符优先级
    OPERATOR_PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        # '^': 3
    }

    def __init__(self):
        self.position = 0
        self.tokens: List[Token] = []

    def tokenize(self, formula: str) -> List[Token]:
        """将公式字符串转换为标记序列"""
        self.position = 0
        self.tokens = []

        while self.position < len(formula):
            char = formula[self.position]

            if char.isspace():
                self.position += 1
                continue

            if char.isdigit() or char == '.':
                self._tokenize_number(formula)
            elif char.isalpha():
                self._tokenize_identifier(formula)
            elif char in '+-*/()[]{}=><^':
                self._tokenize_operator(formula)
            else:
                raise LatexFormatError(f"无法识别的字符: {char} at position {self.position}")
        # print(self.tokens)

        return self.tokens

    def _tokenize_number(self, formula: str):
        """解析数字"""
        start = self.position
        while self.position < len(formula) and (formula[self.position].isdigit() or formula[self.position] == '.'):
            self.position += 1

        number = formula[start:self.position]
        if number.count('.') > 1:
            raise LatexFormatError(f"非法数字格式: {number}")

        self.tokens.append(Token(TokenType.NUMBER, number, start))

    def _tokenize_identifier(self, formula: str):
        """解析标识符（变量名或函数名）"""
        start = self.position
        while self.position < len(formula) and (formula[self.position].isalnum() or formula[self.position] == '_'):
            self.position += 1

        identifier = formula[start:self.position]
        token_type = TokenType.FUNCTION if identifier.lower() in self.LATEX_SYMBOLS else TokenType.VARIABLE
        self.tokens.append(Token(token_type, identifier, start))

    def _tokenize_operator(self, formula: str):
        """解析运算符"""
        start = self.position
        current_char = formula[self.position]
        next_char = formula[self.position + 1] if self.position + 1 < len(formula) else ''

        # 检查双字符运算符
        if current_char + next_char == '**':
            self.tokens.append(Token(TokenType.OPERATOR, '**', start))
            self.position += 2
        elif current_char + next_char in ['>=', '<=', '!=', '==']:
            self.tokens.append(Token(TokenType.OPERATOR, current_char + next_char, start))
            self.position += 2
        else:
            if current_char in '()[]{}':
                token_type = TokenType.BRACKET
            elif current_char in ',':
                token_type = TokenType.DELIMITER
            else:
                token_type = TokenType.OPERATOR

            self.tokens.append(Token(token_type, current_char, start))
            self.position += 1


class LatexFormatter:
    """LaTeX格式转换器"""

    def __init__(self,
                 underscore_to_prime: bool = True,
                 use_frac: bool = False,
                 ignore_multiplication_sign: bool = False,
                 use_dfrac: bool = False,
                 use_slash_as_divisor: bool = False,
                 subscript_rules: Optional[Dict[str, str]] = None,
                 special_var_rules: Optional[Dict[str, Dict[str, str]]] = None):
        self.underscore_to_prime = underscore_to_prime
        self.use_frac = use_frac
        self.ignore_multiplication_sign = ignore_multiplication_sign
        self.use_dfrac = use_dfrac
        self.use_slash_as_divisor = use_slash_as_divisor
        self.subscript_rules = subscript_rules or {}
        self.special_var_rules = special_var_rules or {}
        self.parser = FormulaParser()

    def 统计左括号个数(self, formula: str):
        count = formula.count(' \\left')
        return count

    def 统计右括号个数(self, formula: str):
        count = formula.count(' \\right')
        return count

    def format(self, formula: str) -> str:
        """将公式转换为LaTeX格式"""
        try:
            tokens = self.parser.tokenize(formula)
            return self._process_tokens(tokens)
        except LatexFormatError as e:
            raise e
        except Exception as e:
            raise LatexFormatError(f"转换错误: {str(e)}")

    def replace_from_right(self, s, old, new):
        # 反转字符串
        reversed_s = s[::-1]
        # 反转替换的字符串
        reversed_old = old[::-1]
        reversed_new = new[::-1]
        # 使用 replace 方法进行替换
        replaced_reversed = reversed_s.replace(reversed_old, reversed_new, 1)
        # 再次反转回正常顺序
        return replaced_reversed[::-1]

    def 判断是否需要变成一整个作为分母或分子(self, former, latter):
        # 如果former最前面是左括号且左括号比右括号多一个，latter最后面是右括号且右括号比左括号多一个，则需要变成一整个作为分母或分子
        # print(123, former, latter)
        former_count_left = former.count(' \\left(')
        former_count_right = former.count(' \\right)')
        latter_count_left = latter.count(' \\left(')
        latter_count_right = latter.count(' \\right)')
        # print(456, former_count_left, former_count_right, latter_count_left, latter_count_right)
        if former_count_left - former_count_right == latter_count_right - latter_count_left == 1 and former.startswith(
                ' \\left(') and latter.endswith(' \\right)'):
            # print(123, True)
            return True
        else:
            return False

    def _process_tokens(self, tokens: List[Token]) -> str:
        """处理标记序列"""
        # print(2222, tokens)
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == TokenType.NUMBER:
                result.append(token.value)

            elif token.type == TokenType.VARIABLE:
                result.append(self._process_variable(token.value))

            elif token.type == TokenType.FUNCTION:
                result.append(FormulaParser.LATEX_SYMBOLS.get(
                    token.value.lower(),
                    token.value
                ))

            elif token.type == TokenType.OPERATOR:
                if token.value == '**' or token.value == '^':
                    # 将下一个token转换为上标
                    if i + 1 < len(tokens):
                        next_token = tokens[i + 1]
                        if next_token.type in {TokenType.NUMBER, TokenType.VARIABLE}:
                            value = self._process_tokens([next_token])
                            result[-1] = f"{result[-1]}^{{{value}}}"  # 上标处理
                            i += 2  # 跳过下一个token
                    continue  # 跳过处理运算符
                else:
                    result.append(FormulaParser.LATEX_SYMBOLS.get(
                        token.value,
                        token.value
                    ))

            elif token.type == TokenType.BRACKET:
                if token.value in '({[':
                    result.append('\\left' + token.value)
                else:
                    result.append('\\right' + token.value)

            i += 1

        result = ' '.join(result)
        if self.ignore_multiplication_sign:
            result = result.replace(' \\times', '')
        if self.use_slash_as_divisor:
            result = result.replace('\\div', '/')
        # print(1111, result)
        # if self.use_frac:
        #     if '=' in result:
        #         # print(result)
        #         等号左边, 等号右边 = result.split('=')
        #     else:
        #         等号左边, 等号右边 = '', result
        #     or_res_li = 等号右边.split('\\div')
        #     print(or_res_li)
        #     res_li = []
        #     for i, formula_part in enumerate(or_res_li):
        #         left_count = self.统计左括号个数(formula_part)
        #         right_count = self.统计右括号个数(formula_part)
        #         if left_count != right_count:
        #             # 如果多了左括号，则从左往右删除左括号，直到括号数相等
        #             while left_count > right_count:
        #                 formula_part = formula_part.replace(' \\left(', '', 1)
        #                 left_count -= 1
        #             # 如果多了右括号，则从右往左删除右括号，直到括号数相等
        #             while left_count < right_count:
        #                 formula_part = self.replace_from_right(formula_part, ' \\right)', '')
        #                 right_count -= 1
        #         res_li.append(formula_part)
        #
        #     while len(res_li) > 1:
        #         or_former = or_res_li[-2]
        #         or_latter = or_res_li[-1]
        #         latter = res_li[-1]
        #         former = res_li[-2]
        #         分子, 分母, 前续, 后续 = '', '', '', ''
        #         # 先检查是否有括号
        #         if latter.startswith(' \\left('):
        #             # 分母为括号里面的内容，也就是取左括号和右括号之间的内容
        #             分母 = latter[7:-7]
        #         if former.endswith(' \\right)'):
        #             # 分子为括号里面的内容，也就是取左括号和右括号之间的内容
        #             分子 = former[7:-7]
        #
        #         if not 分母:
        #             latter_li_plus = latter.split('+')
        #             latter_li_minus = latter.split('-')
        #             分母1 = latter_li_plus[0]
        #             分母2 = latter_li_minus[0]
        #             分母 = 分母1 if len(分母1) < len(分母2) else 分母2
        #             if 分母 == 分母1:
        #                 后续 = '+'.join(latter_li_plus[1:])
        #             else:
        #                 后续 = '-'.join(latter_li_minus[1:])
        #         if not 分子:
        #             former_li_plus = former.split('+')
        #             former_li_minus = former.split('-')
        #             分子1 = former_li_plus[-1]
        #             分子2 = former_li_minus[-1]
        #             分子 = 分子1 if len(分子1) < len(分子2) else 分子2
        #             if 分子 == 分子1:
        #                 前续 = '+'.join(former_li_plus[:-1]) + '+'
        #             else:
        #                 前续 = '-' + '-'.join(former_li_minus[:-1])
        #
        #         # print(11111, former, latter, 分子, 分母)
        #         # print(22222, 前续)
        #         # print(33333, 后续)
        #
        #         if 分子 and 分母:
        #             分数 = f"\\frac{{{分子}}}{{{分母}}}"
        #         else:
        #             raise LatexFormatError(f"分数化错误: {former, latter}")
        #
        #         后两个分数化结果 = 前续 + 分数 + 后续
        #         # print(44444, 后两个分数化结果)
        #         if self.判断是否需要变成一整个作为分母或分子(or_former, or_latter):
        #             后两个分数化结果 = f" \\left({后两个分数化结果} \\right)"
        #         print(55555, 后两个分数化结果)
        #         res_li[-2] = 后两个分数化结果
        #         res_li.pop()
        #     if 等号左边:
        #         result = 等号左边 + '=' + res_li[0]
        #     else:
        #         result = res_li[0]

        return result

    def _process_variable(self, var: str) -> str:
        """处理变量"""
        # 检查特殊规则
        # print(var)
        if var in self.special_var_rules:
            return self._apply_special_rules(var)

        # # 处理结尾的下划线
        # if self.underscore_to_prime:
        #     # 查找字符串末尾的下划线数量
        #     underscore_count = 0
        #     while var and var[-1] == '_':
        #         underscore_count += 1
        #         var = var[:-1]  # 移除末尾的下划线
        #
        #     # 如果有下划线，替换为一个^{\\prime}
        #     if underscore_count > 0:
        #         var += "^{\\prime}"
        #         return var

        # 处理一般规则
        return self._apply_general_rules(var)

    def _apply_special_rules(self, var: str) -> str:
        """应用特殊规则"""
        base = var[0]
        trailing = var[1:] if len(var) > 1 else ''
        underscore_count = 0
        if not trailing:
            return base

        result = base
        var_rules = self.special_var_rules[var]
        if self.underscore_to_prime:

            while trailing and trailing[-1] == '_':
                underscore_count += 1
                trailing = trailing[:-1]  # 移除末尾的下划线

        for i, char in enumerate(trailing):
            if char == '_':
                result += '_{\\_}'
                continue
            rule = var_rules.get(str(i), self.subscript_rules.get(str(i), '_'))
            result += self._format_char(char, rule)
        if underscore_count > 0:
            result += "^{\\prime}"
        return result

    def _apply_general_rules(self, var: str) -> str:
        """应用一般规则"""
        # print(1111, var)
        base = var[0]
        trailing = var[1:] if len(var) > 1 else ''
        underscore_count = 0
        if not trailing:
            return base
        if self.underscore_to_prime:
            while trailing and trailing[-1] == '_':
                trailing = trailing[:-1]  # 移除末尾的下划线
                underscore_count += 1
        result = base
        for i, char in enumerate(trailing):
            if char == '_':
                result += '_{\\_}'
                continue
            rule = self.subscript_rules.get(str(i), '_')
            result += self._format_char(char, rule)
        if underscore_count > 0:
            result += "^{\\prime}"
        return result

    def _format_char(self, char: str, rule: str) -> str:
        """格式化字符"""
        if rule == '_':
            return f"_{{{char}}}"
        elif rule == '^':
            return f"^{{{char}}}"
        else:
            return char


def formula_to_latex(formula_str: str,
                     underscore_to_prime: bool = True,
                     use_frac: bool = False,
                     use_slash_as_divisor: bool = False,
                     ignore_multiplication_sign: bool = False,
                     use_dfrac: bool = False,
                     subscript_rules: Optional[Dict[str, str]] = None,
                     special_var_rules: Optional[Dict[str, Dict[str, str]]] = None) -> str:
    """
    将字符串公式转换为LaTeX格式

    参数:
        formula_str: 原始公式字符串
        underscore_to_prime: 是否将_转换为撇号(')
        subscript_rules: 字典，指定变量后续字符的格式{'0': '^', '1': '_', ...}
        special_var_rules: 字典，为特定变量指定规则，格式为{'变量名': {'0': 规则, '1': 规则}}

    返回:
        LaTeX格式的字符串

    异常:
        LatexFormatError: 当转换过程中发生错误时
    """
    formatter = LatexFormatter(
        underscore_to_prime=underscore_to_prime,
        use_frac=use_frac,
        ignore_multiplication_sign=ignore_multiplication_sign,
        use_dfrac=use_dfrac,
        use_slash_as_divisor=use_slash_as_divisor,
        subscript_rules=subscript_rules,
        special_var_rules=special_var_rules
    )
    return formatter.format(formula_str)


if __name__ == '__main__':
    # 基本使用
    formula = "Es = αcr * ψ * σsq / Es * (1.9 * cs + 0.08 * deq / ρte) = 0.01775 / (1 + 0.0337 * 20.1 + 0.000221 * 20.1^2) = 11111kN/mm**2"
    rules = {
        '0': '^',
        '1': '_'
    }
    special_rules = {
        'mm': {
            '0': '',
            '1': ''
        },
        'kN': {
            '0': '',
            '1': ''
        }
    }
    print('$$' + formula_to_latex(
        formula,
        ignore_multiplication_sign=False,
        use_slash_as_divisor=True,
        # use_frac=True,
        # subscript_rules=rules,
        special_var_rules=special_rules
    ) + '$$')

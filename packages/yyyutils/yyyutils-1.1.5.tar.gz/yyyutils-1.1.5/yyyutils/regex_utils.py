import re
from typing import Dict


class RegexUtils:
    @staticmethod
    def test_regex(regex_pattern, string):
        pattern = re.compile(regex_pattern)
        match = pattern.search(string)  # 匹配字符串中第一个符合正则表达式的子串，返回一个Match对象
        if match:
            return match.group()  # 返回匹配的子串
        else:
            return None

    @staticmethod
    def extract_exponents(string: str) -> Dict[str, int]:
        """
        提取字符串表达式中变量的指数
        :param string:
        :return:
        """
        string = str(string)
        var_dict = {}

        # 处理分子
        numerator = string.split('/')[0]  # 取分子部分
        # 使用正则表达式匹配基本单位和可能的指数
        pattern = r'([LMT])(?:\^(-?\d+)|\*\*(-?\d+))?'

        # 从分子解析
        for match in re.findall(pattern, numerator):
            base = match[0]
            exponent = int(match[1] or match[2] or 1)  # 默认指数为1
            if base not in var_dict:
                var_dict[base] = 0
            var_dict[base] += exponent  # 加累加指数

        # 处理分母
        if '/' in string:
            denominator = string.split('/')[1]  # 取分母部分
            for match in re.findall(pattern, denominator):
                base = match[0]
                exponent = int(match[1] or match[2] or 1)  # 默认指数为1
                if base not in var_dict:
                    var_dict[base] = 0
                var_dict[base] -= exponent  # 减少指数

        return var_dict


import re
from typing import List, Tuple, Dict, Optional, NamedTuple
from itertools import count


class Pattern(NamedTuple):
    pattern: str
    should_match: bool


def generate_regex_advanced(patterns: List[Pattern]) -> Tuple[str, List[str]]:
    def pattern_to_regex(pattern: str, group_counter: count) -> Tuple[str, Dict[str, str]]:
        parts = re.split(r'(\{.*?\})', pattern)
        regex_parts = []
        variables = {}
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                var_name = part[1:-1]
                if var_name not in variables:
                    group_name = f"{var_name}_{next(group_counter)}"
                    variables[var_name] = f'(?P<{group_name}>[^\\s]+)'
                regex_parts.append(variables[var_name])
            else:
                regex_parts.append(re.escape(part))
        return ''.join(regex_parts), variables

    positive_patterns = []
    negative_patterns = []
    all_variables = set()
    group_counter = count(1)

    for pattern in patterns:
        regex, vars = pattern_to_regex(pattern.pattern, group_counter)
        all_variables.update(vars.keys())
        if pattern.should_match:
            positive_patterns.append(regex)
        else:
            negative_patterns.append(f'(?!{regex})')

    positive_part = '|'.join(f'(?:{p})' for p in positive_patterns) if positive_patterns else '(?!)'
    negative_part = ''.join(negative_patterns)

    final_regex = f'^{negative_part}(?:{positive_part})$'
    return final_regex, list(all_variables)


def generate_regex_from_match(full_string: str, matched_string: str, exact_match: bool = False) -> str:
    if matched_string not in full_string:
        raise ValueError("Matched string must be a part of the full string")

    escaped_full = re.escape(full_string)
    escaped_match = re.escape(matched_string)

    if exact_match:
        pattern = escaped_full.replace(escaped_match, '(.+?)', 1)  # Replace only the first occurrence
    else:
        parts = escaped_full.split(escaped_match)
        pattern = '(.*)'.join(parts)

    return f'^{pattern}$'


def test_regex(regex: str, variables: List[str], test_strings: List[str]) -> None:
    for string in test_strings:
        match = re.match(regex, string)
        print(f"\nString: {string}")
        print(f"Matches: {bool(match)}")
        if match:
            for var in variables:
                group_name = next((key for key in match.groupdict().keys() if key.startswith(var)), None)
                if group_name and group_name in match.groupdict():
                    print(f"  {var}: {match.group(group_name)}")


def test_regex_from_match(regex: str, test_strings: List[str]) -> None:
    for string in test_strings:
        match = re.match(regex, string)
        print(f"\nString: {string}")
        print(f"Matches: {bool(match)}")
        if match and match.groups():
            print(f"  Matched part: {match.group(1)}")


import re
from typing import List, Tuple


def generate_regex_from_match(full_string: str, matched_string: str, exact_match: bool = False,
                              context_chars: int = 0) -> str:
    if matched_string not in full_string:
        raise ValueError("Matched string must be a part of the full string")

    start_index = full_string.index(matched_string)
    end_index = start_index + len(matched_string)

    # Determine the context range
    context_start = max(0, start_index - context_chars)
    context_end = min(len(full_string), end_index + context_chars)

    # Extract the relevant part of the string
    relevant_string = full_string[context_start:context_end]

    # Adjust the matched_string position in the relevant_string
    adjusted_start = start_index - context_start
    adjusted_end = adjusted_start + len(matched_string)

    before = re.escape(relevant_string[:adjusted_start])
    after = re.escape(relevant_string[adjusted_end:])

    if exact_match:
        pattern = before + '(.+?)' + after
    else:
        pattern = before + '(.*)' + after

    return f'^{pattern}$' if context_chars == 0 else pattern


def test_regex_from_match(regex: str, test_strings: List[str]) -> None:
    for string in test_strings:
        match = re.search(regex, string)
        print(f"\nString: {string}")
        print(f"Matches: {bool(match)}")
        if match and match.groups():
            print(f"  Matched part(s): {match.groups()}")


def main():
    # Test with a long string
    long_string = "This is a very long string with [PLACEHOLDER] near the beginning. " \
                  "The rest of the string contains a lot of irrelevant information. " \
                  "We don't need to include all of this in our regular expression. " \
                  "This makes our regex much more efficient and easier to read."
    placeholder = "[PLACEHOLDER]"

    # Generate regex with different context sizes
    regex_full = generate_regex_from_match(long_string, placeholder, exact_match=False)
    regex_context_10 = generate_regex_from_match(long_string, placeholder, exact_match=False, context_chars=10)
    regex_context_20 = generate_regex_from_match(long_string, placeholder, exact_match=False, context_chars=20)

    print(f"Full regex: {regex_full}")
    print(f"Regex with 10 context chars: {regex_context_10}")
    print(f"Regex with 20 context chars: {regex_context_20}")

    test_strings = [
        long_string,
        long_string.replace("[PLACEHOLDER]", "variable"),
        "This is a different string with [PLACEHOLDER] near the beginning.",
        "This string doesn't match the pattern at all."
    ]

    print("\nTesting regex with 10 context chars:")
    test_regex_from_match(regex_context_10, test_strings)

    print("\nTesting regex with 20 context chars:")
    test_regex_from_match(regex_context_20, test_strings)


if __name__ == "__main__":
    main()

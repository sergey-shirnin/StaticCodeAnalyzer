import re
import ast


def check_s001(line: str, line_ind: int, lines: list, max_length=79) -> str | None:
    if len(line) > max_length:
        return f'Line {line_ind + 1}: S001 Too long'
    return None

def check_s002(line: str, line_ind: int, lines: list, multiple=4) -> str | None:
    indent = len(line) - len(line.lstrip())
    if line != '\n' and indent % multiple:
        return f'Line {line_ind + 1}: S002 Indentation is not a multiple of four'
    return None

def check_s003(line: str, line_ind: int, lines: list) -> str | None:
    if ';' in line:
        line_ch = [ch for ch in line if ch in ('"', "'", '#', ';')]
        is_in_string = True if (line_ch[line_ch.index(';') + 1:].count("'") +
                                line_ch[line_ch.index(';') + 1:].count('"')) % 2 else False
        is_in_comment = True if '#' in line_ch[:line_ch.index(';') + 1] and not is_in_string else False
        if not is_in_string and not is_in_comment:
            return f'Line {line_ind + 1}: S003 Unnecessary semicolon'
        return None

def check_s004(line: str, line_ind: int, lines: list) -> str | None:
    if '#' in line and line.index('#') > 1 and not re.match(r'.+\s{2,}#.*', line):
        return f'Line {line_ind + 1}: S004 At least two spaces required before inline comments'
    return None

def check_s005(line: str, line_ind: int, lines: list) -> str | None:
    if '#' in line and re.match(r'.*todo.*', line[line.index('#') + 1:], flags=re.I):
        return f'Line {line_ind + 1}: S005 TODO found'
    return None

def check_s006(line: str, line_ind: int, lines: list) -> str | None:
    if line_ind > 2 and all(['blank' if lines[line_ind - i] == '\n' else '' for i in range(1, 4)]):
        return f'Line {line_ind + 1}: S006 More than two blank lines used before this line'
    return None

def check_s007(line: str, line_ind: int, lines: list) -> str | None:
    if re.match(r'^(class|def)\s\s+', line.lstrip()):
        construction_name = line.lstrip().split()[0]
        return f"Line {line_ind + 1}: S007 Too many spaces after '{construction_name}'"
    return None

def check_s008(line: str, line_ind: int, lines: list) -> str | None:
    if re.match(r'^class\s+[a-z]', line.lstrip()):
        class_name = line.lstrip().split()[1]
        return f"Line {line_ind + 1}: S008 Class name '{class_name}' should use CamelCase"
    return None

def check_s009(line: str, line_ind: int, lines: list) -> str | None:
    if re.match(r'^def\s+[A-Z]', line.lstrip()):
        def_name = line.lstrip().split()[1]
        return f"Line {line_ind + 1}: S009 Function name '{def_name}' should use snake_case"
    return None

def check_s010(tree) -> list:
    res = []
    for el in ast.walk(tree):
        if isinstance(el, ast.FunctionDef):
            for argument_name in [a.arg for a in el.args.args]:
                if re.match(r'^[A-Z]', argument_name):
                    res.append(f"Line {el.lineno}: S010 Argument name '{argument_name}' should be written snake_case")
    return res


def check_s011(tree) -> list:
    res = []
    for el in ast.walk(tree):
        if isinstance(el, ast.Name) and isinstance(el.ctx, ast.Store):
            variable_name = el.id
            if re.match(r'^[A-Z]', variable_name):
                res.append(f"Line {el.lineno}: S011 Variable name '{variable_name}' should be written snake_case")
    return res


def check_s012(tree) -> list:
    res = []
    for el in ast.walk(tree):
        if isinstance(el, ast.FunctionDef):
            for item in el.args.defaults:
                if isinstance(item, ast.List):
                    res.append(f"Line {el.lineno}: S012 Default argument value is mutable")
    return res

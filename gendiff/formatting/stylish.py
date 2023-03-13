import json


def stylish(diff, depth=1):
    ans = ''
    for i in sorted(diff):
        gap = ('    ' * depth)
        gap2 = gap[2:]
        if isinstance(diff[i], dict) and "status" not in diff[i]:
            ans += f"{gap}{i}: {{\n"
            ans += stringify(stylish(diff[i], depth + 1), depth)
            ans += f"\n{gap}}}\n"
        elif diff[i]['status'] == 'added':
            ans += auto_space(gap2, i, stringify(diff[i]['new_value'], depth),
                              "+ ")
        elif diff[i]['status'] == 'removed':
            ans += auto_space(gap2, i, stringify(diff[i]['old_value'], depth),
                              "- ")
        elif diff[i]['status'] == 'modified':
            ans += auto_space(gap2, i, stringify(diff[i]['old_value'], depth),
                              "- ")
            ans += auto_space(gap2, i, stringify(diff[i]['new_value'], depth),
                              "+ ")
        elif diff[i]['status'] == 'not changed':
            ans += auto_space(gap, i, stringify(diff[i]['data'], depth))
    if ans[-1:] == "\n":
        ans = ans[:-1]
    if depth == 1:
        return "{\n" + ans + "\n}"
    return ans


def auto_space(gap, i, value, sign=""):
    if value != "":
        return f"{gap}{sign}{i}: {value}\n"
    return f"{gap}{sign}{i}:\n"


def stringify(raw_value, depth):
    if isinstance(raw_value, dict):
        normalized = "{\n"
        normalized += get_tree(raw_value, depth + 1)
        normalized += f"{depth * '    '}}}"
    elif isinstance(raw_value, tuple):
        normalized = (stringify(raw_value[0], depth),
                      stringify(raw_value[1], depth))
    else:
        normalized = fix(raw_value)
    return normalized


def get_tree(value, depth=0):
    tree = ""
    for nested_key, nested_value in value.items():
        if isinstance(nested_value, dict):
            tree += f"{depth * '    '}{nested_key}: {{\n"
            tree += f"{get_tree(nested_value, depth + 1)}"
            tree += f"{depth * '    '}}}\n"
        else:
            nested_value = json.dumps(nested_value).strip('"')
            tree += auto_space(depth * '    ', nested_key, fix(nested_value))
    return tree


def fix(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return value

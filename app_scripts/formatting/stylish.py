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
            if diff[i]['new_value'] != "":
                ans += f"{gap2}+ {i}: " \
                       f"{stringify(diff[i]['new_value'], depth)}\n"
            else:
                ans += f"{gap2}+ {i}:\n"
        elif diff[i]['status'] == 'removed':
            if diff[i]['old_value'] != "":
                ans += f"{gap2}- {i}:" \
                       f" {stringify(diff[i]['old_value'], depth)}\n"
            else:
                ans += f"{gap2}- {i}:\n"
        elif diff[i]['status'] == 'modified':
            if diff[i]['old_value'] != "":
                ans += f"{gap2}- {i}:" \
                       f" {stringify(diff[i]['old_value'], depth)}\n"
            else:
                ans += f"{gap2}- {i}:\n"
            if diff[i]['new_value'] != "":
                ans += f"{gap2}+ {i}:" \
                       f" {stringify(diff[i]['new_value'], depth)}\n"
            else:
                ans += f"{gap2}+ {i}:\n"
        elif diff[i]['status'] == 'not changed':
            ans += f"{gap}{i}: {stringify(diff[i]['data'], depth)}\n"
        else:
            ans += f"{gap}{i}: {stringify(diff[i]['data'], depth)}\n"
    if ans[-1:] == "\n":
        ans = ans[:-1]
    if depth == 1:
        return "{\n" + ans + "\n}"
    return ans


def stringify(raw_value, depth):
    if isinstance(raw_value, dict):
        normalized_value = "{\n"
        normalized_value += get_tree(raw_value, depth + 1)
        normalized_value += f"{depth * '    '}}}"
    elif isinstance(raw_value, tuple):
        normalized_value = (stringify(raw_value[0], depth),
                            stringify(raw_value[1], depth))
    else:
        normalized_value = fix(raw_value)
    return normalized_value


def get_tree(value, depth=0):
    tree = ""
    for nested_key, nested_value in value.items():
        if isinstance(nested_value, dict):
            tree += f"{depth * '    '}{nested_key}: {{\n"
            tree += f"{get_tree(nested_value, depth + 1)}"
            tree += f"{depth * '    '}}}\n"
        else:
            nested_value = json.dumps(nested_value).strip('"')
            tree += f"{depth * '    '}{nested_key}: {fix(nested_value)}\n"
    return tree


def fix(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return value

import argparse
import json
import yaml


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', help='Path to the first file')
    parser.add_argument('second_file', help='Path to the second file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


def generate_diff(file1, file2):
    formatter = stylish
    extension = file1.split(".")[-1]
    if extension == 'json':
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        return formatter(get_diff(data1, data2))

    elif extension == 'yaml':
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = yaml.safe_load(f1.read())
            data2 = yaml.safe_load(f2.read())
        return formatter(get_diff(data1, data2))

    else:
        print(f"{extension} files are not supported.")


def get_diff(dict1, dict2):
    diff = {}

    # Iterate over keys in first dict
    for key in dict1:
        if key not in dict2:
            diff[key] = {"status": "removed", "old_value": dict1[key]}
        elif dict1[key] != dict2[key]:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                # Recursively compare nested dictionaries
                nested_diff = get_diff(dict1[key], dict2[key])
                if nested_diff:
                    diff[key] = nested_diff
            else:
                diff[key] = {"status": "modified", "old_value": dict1[key],
                             "new_value": dict2[key]}
        else:
            diff[key] = {"status": "not changed", "data": dict1[key]}

    # Iterate over keys in second dict
    for key in dict2:
        if key not in dict1:
            diff[key] = {"status": "added", "new_value": dict2[key]}

    return diff


def stylish(diff, depth=1):
    "convert only dict to stylish format"
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


if __name__ == '__main__':
    main()

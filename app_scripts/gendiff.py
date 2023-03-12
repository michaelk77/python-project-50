import argparse
import json
import yaml
from app_scripts.formatting.stylish import stylish
from app_scripts.formatting.plain import plain

all_formatters = {
    "stylish": stylish,
    "plain": plain
}


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', help='Path to the first file')
    parser.add_argument('second_file', help='Path to the second file')
    parser.add_argument('-f', '--format', choices=["stylish", "plain"],
                        default="stylish", help='set format of output')

    args = parser.parse_args()
    formatter = args.format
    print(generate_diff(args.first_file, args.second_file, formatter))


def generate_diff(file1, file2, format="stylish"):
    formatter = all_formatters[format]
    extension = file1.split(".")[-1]
    if extension == 'json':
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        return formatter(get_diff(data1, data2))

    elif extension == 'yaml' or extension == 'yml':
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


if __name__ == '__main__':
    main()

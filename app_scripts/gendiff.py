import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', help='Path to the first file')
    parser.add_argument('second_file', help='Path to the second file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()

    if ".json" in args.first_file and ".json" in args.second_file:
        print(generate_diff(args.first_file, args.second_file))
    # TODO: Implement file comparison logic here


def generate_diff(filepath1, filepath2):
    data1 = read_file(filepath1)
    data2 = read_file(filepath2)
    diff = get_diff(data1, data2)
    return format_diff(diff)


def read_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def get_diff(data1, data2):
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    common_keys = keys1 & keys2
    added_keys = keys2 - keys1
    removed_keys = keys1 - keys2

    diff = []
    for key in sorted(common_keys):
        if data1[key] != data2[key]:
            diff.append({
                'key': key,
                'type': 'modified',
                'old_value': data1[key],
                'new_value': data2[key],
            })
        else:
            diff.append({
                'key': key,
                'type': 'unchanged',
                'value': data1[key],
            })

    for key in sorted(added_keys):
        diff.append({
            'key': key,
            'type': 'added',
            'value': data2[key],
        })

    for key in sorted(removed_keys):
        diff.append({
            'key': key,
            'type': 'removed',
            'value': data1[key],
        })

    return diff


def format_diff(diff):
    lines = []
    for item in sorted(diff, key=lambda x: x['key']):
        key = item['key']
        type_ = item['type']
        value = item.get('value')
        old_value = item.get('old_value')
        new_value = item.get('new_value')

        if type_ == 'added':
            lines.append(f'  + {key}: {format_value(value)}')
        elif type_ == 'removed':
            lines.append(f'  - {key}: {format_value(value)}')
        elif type_ == 'modified':
            lines.append(f'  - {key}: {format_value(old_value)}')
            lines.append(f'  + {key}: {format_value(new_value)}')
        else:
            lines.append(f'    {key}: {format_value(value)}')

    return '{\n' + '\n'.join(lines) + '\n}'


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


if __name__ == '__main__':
    main()

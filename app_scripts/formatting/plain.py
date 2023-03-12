import json


def plain(diff, path=""):
    formatter = ""
    if isinstance(diff, dict):
        for i in sorted(diff):
            if isinstance(diff[i], dict) and "status" not in diff[i]:
                if path:
                    formatter += plain(diff[i], path + "." + i) + "\n"
                else:
                    formatter += plain(diff[i], i) + "\n"
            elif isinstance(diff[i], dict):
                status = diff[i]['status']
                dot = "." if path else ""
                if status == "removed":
                    formatter += f"Property '{path}{dot}{i}' was removed\n"
                elif status == "added":
                    formatter += f"Property '{path}{dot}{i}'" \
                                 f" was added with value: "
                    formatter += f"{stringify(diff[i]['new_value'])}\n"
                elif status == "deleted":
                    formatter += f"Property '{path}{dot}{i}' was removed\n"
                elif status == "modified":
                    formatter += f"Property '{path}{dot}{i}' was updated. "
                    formatter += f"From {stringify(diff[i]['old_value'])} " \
                                 f"to {stringify(diff[i]['new_value'])}\n"

    return formatter.strip()


def stringify(raw_value):
    if isinstance(raw_value, dict):
        normalized = "[complex value]"
    elif isinstance(raw_value, bool) or not raw_value:
        normalized = json.dumps(raw_value).strip('"')
    elif isinstance(raw_value, str):
        raw_value = json.dumps(raw_value).strip('"')
        normalized = f"'{raw_value}'"
    else:
        normalized = raw_value
    if not raw_value and not normalized:
        normalized = "''"
    return normalized

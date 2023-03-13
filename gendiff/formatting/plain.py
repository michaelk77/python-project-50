import json


def plain(diff, path=""):
    """formatting diff to plain style string"""
    ans = ""
    if isinstance(diff, dict):
        for i in sorted(diff):
            if isinstance(diff[i], dict) and "status" not in diff[i]:
                ans += plain(diff[i], path_ans(path, i, ".")) + "\n"
            else:
                ans = status_analise(diff, i, path, ans)

    return ans.strip()


def path_ans(path, i, dot):
    """Return path with dot or not"""
    if path:
        return f"{path}{dot}{i}"
    return i


def status_analise(diff, i, path, ans):
    """Analise's status of diff and return string"""
    if isinstance(diff[i], dict):
        status = diff[i]['status']
        dot = "." if path else ""
        if status == "removed":
            ans += f"Property '{path}{dot}{i}' was removed\n"
        elif status == "added":
            ans += f"Property '{path}{dot}{i}'" \
                   f" was added with value: "
            ans += f"{stringify(diff[i]['new_value'])}\n"
        elif status == "deleted":
            ans += f"Property '{path}{dot}{i}' was removed\n"
        elif status == "modified":
            ans += f"Property '{path}{dot}{i}' was updated. "
            ans += f"From {stringify(diff[i]['old_value'])} " \
                   f"to {stringify(diff[i]['new_value'])}\n"
    return ans


def stringify(raw_value):
    """Return string from raw_value"""
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

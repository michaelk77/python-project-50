import pytest
from app_scripts.gendiff import generate_diff

test_data = [("tests/fixtures/file1.json", "tests/fixtures/file2.json",
              "tests/fixtures/file3.txt")]


@pytest.mark.parametrize("filepath1, filepath2, expected", test_data)
def test_generate_diff(filepath1, filepath2, expected):
    diff = generate_diff(filepath1, filepath2)
    with open(expected, 'r') as f:
        ans = f.read()
    assert diff == ans
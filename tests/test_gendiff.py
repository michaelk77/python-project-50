import pytest
from gendiff.generate_diff import generate_diff

test_data = [("tests/fixtures/file1.json", "tests/fixtures/file2.json",
              "tests/fixtures/file3.txt", "stylish"), (
                 "tests/fixtures/file4.yaml", "tests/fixtures/file5.yaml",
                 "tests/fixtures/file6.txt", "stylish"),
             ("tests/fixtures/file1.json", "tests/fixtures/file2.json",
              "tests/fixtures/file7.txt", "plain"), ("tests/fixtures/file1.json", "tests/fixtures/file2.json",
              "tests/fixtures/file8.txt", "json")]


@pytest.mark.parametrize("filepath1, filepath2, expected, format", test_data)
def test_generate_diff(filepath1, filepath2, expected, format):
    diff = generate_diff(filepath1, filepath2, format)
    with open(expected, 'r') as f:
        ans = f.read()
    assert diff == ans

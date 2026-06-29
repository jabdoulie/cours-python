import subprocess
import pytest

@pytest.mark.parametrize("name, expected", [
    ("Alice", "Hello, Alice!"),
    ("Bob", "Hello, Bob!")
])
def test_greet_cli(name, expected):
    result = subprocess.run(["python3", "cli_tool.py", name], capture_output=True, text=True)
    assert result.stdout.strip() == expected
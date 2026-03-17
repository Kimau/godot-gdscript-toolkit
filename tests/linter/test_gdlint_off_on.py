import pytest

from .common import simple_ok_check


# fmt: off
@pytest.mark.parametrize("code", [
# All problems suppressed inside off/on block
"""
# gdlint: off
func Bad_Name():
    pass
# gdlint: on
""",
# No-colon variant
"""
#gdlint off
func Bad_Name():
    pass
#gdlint on
""",
# Off at EOF suppresses problems to end of file
"""
# gdlint: off
func Bad_Name():
    pass
""",
# Code outside disabled region is fine if it has no problems
"""
func good_name():
    pass
# gdlint: off
func Bad_Name():
    pass
# gdlint: on
""",
])
# fmt: on
def test_gdlint_off_suppresses_problems(code):
    simple_ok_check(code)


def test_gdlint_off_only_suppresses_in_region():
    """Problems outside the off/on region are still reported."""
    from gdtoolkit.linter import lint_code

    code = "func Bad_Name():\n    pass\n# gdlint: off\nfunc Another_Bad():\n    pass\n# gdlint: on\n"
    problems = lint_code(code)
    assert len(problems) == 1
    assert problems[0].name == "function-name"
    assert problems[0].line == 1

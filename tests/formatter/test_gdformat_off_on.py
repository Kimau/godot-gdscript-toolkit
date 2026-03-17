import pytest

from .common import format_and_compare


# fmt: off
@pytest.mark.parametrize("input_code,expected_output_code", [
# Disabled region is preserved verbatim (bad spacing kept)
(
"""var x = 1
# gdformat: off
var y=1+2+3
# gdformat: on
var z = 3
""",
"""var x = 1
# gdformat: off
var y=1+2+3
# gdformat: on
var z = 3
""",
),
# No-colon variant also works
(
"""var x = 1
#gdformat off
var y=1+2+3
#gdformat on
var z = 3
""",
"""var x = 1
#gdformat off
var y=1+2+3
#gdformat on
var z = 3
""",
),
# Off at EOF (no matching on) — rest of file preserved verbatim
(
"""var x = 1
# gdformat: off
var y=1+2+3
""",
"""var x = 1
# gdformat: off
var y=1+2+3
""",
),
# Code outside disabled region is still formatted
(
"""var x=1
# gdformat: off
var y=1+2+3
# gdformat: on
var z=3
""",
"""var x = 1
# gdformat: off
var y=1+2+3
# gdformat: on
var z = 3
""",
),
# Normal formatting still works with no markers
(
"""var x=1
""",
"""var x = 1
""",
),
])
# fmt: on
def test_gdformat_off_on(input_code, expected_output_code):
    format_and_compare(input_code, expected_output_code)


def test_gdformat_off_on_is_stable():
    """Formatting a file with off/on markers twice gives the same result."""
    from gdtoolkit.formatter import format_code

    code = "var x = 1\n# gdformat: off\nvar y=1+2+3\n# gdformat: on\nvar z = 3\n"
    first_pass = format_code(code, max_line_length=100)
    second_pass = format_code(first_pass, max_line_length=100)
    assert first_pass == second_pass, "Formatter is not stable with off/on regions"

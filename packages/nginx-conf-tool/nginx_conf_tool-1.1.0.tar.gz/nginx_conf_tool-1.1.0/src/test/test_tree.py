import pytest
from click.testing import CliRunner

from nginx_conf_tool.tree import tree


@pytest.mark.parametrize(
    ["args", "expected_code", "expected_output_file"],
    [
        pytest.param([], 2, "", id="missing file"),
        pytest.param(["samples/simple.conf"], 0, "simple_output.txt", id="no option"),
        pytest.param(
            ["-d", "samples/simple.conf"], 0, "simple_dir_only.txt", id="-d option"
        ),
        pytest.param(
            ["-L", "1", "samples/simple.conf"], 0, "simple_level1.txt", id="-L option"
        ),
        pytest.param(["samples/faulty.conf"], 1, "", id="file with error"),
    ],
)
def test_simple_verify_stdout(request, args, expected_code, expected_output_file):
    runner = CliRunner()
    result = runner.invoke(tree, args=args)

    assert result.exit_code == expected_code

    if expected_code == 0:
        data_dir = request.path.parent / "data"
        expected = (data_dir / expected_output_file).read_text()
        assert result.output == expected

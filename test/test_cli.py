import pytest
from click.testing import CliRunner

from buck import cli


def test_cli_list_all(mocker):
    mocker.patch("buck_aws.list_all_in_bucket", return_value=["file1", "file2"])
    runner = CliRunner()
    result = runner.invoke(cli, ["list_all"])
    assert result.exit_code == 0
    assert result.output == "['file1', 'file2']\n"

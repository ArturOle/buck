import pytest
from click.testing import CliRunner

from buck import cli


# Correct tests

def test_cli_list_all_correct(mocker):
    mocker.patch("buck_aws.list_all_in_bucket", return_value=["file1", "file2"])
    runner = CliRunner()
    result = runner.invoke(cli, ["list-all"])
    assert result.exit_code == 0
    assert result.output == "['file1', 'file2']\n"

def test_cli_find_correct(mocker):
    mocker.patch("buck_aws.find_in_bucket", return_value="file1")
    runner = CliRunner()
    result = runner.invoke(cli, ["find", "--pattern", ".*"])
    assert result.exit_code == 0
    assert result.output == "file1\n"

def test_cli_upload_correct(mocker):
    mocker.patch("buck_aws.upload_file_to_bucket", return_value="File file1 uploaded")
    runner = CliRunner()
    result = runner.invoke(cli, ["upload", "--file-path", "file1"])
    assert result.exit_code == 0
    assert result.output == "File file1 uploaded\n"

def test_cli_delete_correct(mocker):
    mocker.patch("buck_aws.delete_matching_files", return_value="Deleted file1")
    runner = CliRunner()
    result = runner.invoke(cli, ["delete", "--pattern", "\b\B"])
    assert result.exit_code == 0
    assert result.output == "Deleted file1\n"


# Incorrect tests

def test_cli_list_all_incorrect(mocker):
    mocker.patch("buck_aws.list_all_in_bucket", return_value=None)
    runner = CliRunner()
    result = runner.invoke(cli, ["list_all", "arg1"])
    assert result.exit_code == 2


def test_cli_find_incorrect(mocker):
    mocker.patch("buck_aws.find_in_bucket", return_value=None)
    runner = CliRunner()
    result = runner.invoke(cli, ["find"])
    assert result.exit_code == 2


def test_cli_upload_incorrect(mocker):
    mocker.patch("buck_aws.upload_file_to_bucket", return_value=None)
    runner = CliRunner()
    result = runner.invoke(cli, ["upload"])
    assert result.exit_code == 2


def test_cli_delete_incorrect(mocker):
    mocker.patch("buck_aws.delete_matching_files", return_value=None)
    runner = CliRunner()
    result = runner.invoke(cli, ["delete"])
    assert result.exit_code == 2

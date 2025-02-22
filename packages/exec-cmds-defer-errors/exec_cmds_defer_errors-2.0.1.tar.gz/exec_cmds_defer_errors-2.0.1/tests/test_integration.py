"""
Integration tests for the `exec_cmds_defer_errors` module.
"""

import click
from click.testing import CliRunner

from exec_cmds_defer_errors.exec_cmds_defer_errors import (
    Command,
    exec_cmds_defer_errors,
)


def test_cli_help() -> None:
    """Test the CLI help message."""

    result = CliRunner().invoke(exec_cmds_defer_errors, ["--help"])

    assert result.exit_code == 0


def test_command() -> None:
    """
    Test that the custom command handles missing epilog.
    """

    @click.command(
        cls=Command,
    )
    def command() -> None:
        pass

    CliRunner().invoke(command, ["--help"])


def test_first_cmd_error() -> None:
    """
    Test that subsequent commands are executed even if the first command fails.
    """

    result = CliRunner().invoke(
        exec_cmds_defer_errors,
        ["exit 1", "echo lol"],
    )

    assert "1 out of 2 command(s) failed." in result.output
    assert "Executed command 1 failed with exit code 1" in result.output
    assert "Executed command 2 successfully" in result.output

    assert result.exit_code == 1


def test_multiple_cmd_error() -> None:
    """
    Test correct handling of multiple commands failing.
    """

    result = CliRunner().invoke(
        exec_cmds_defer_errors,
        ["exit 1", "exit 2"],
    )

    assert "2 out of 2 command(s) failed." in result.stdout
    assert "Executed command 1 failed with exit code 1" in result.output
    assert "Executed command 2 failed with exit code 2" in result.output

    assert result.exit_code == 1


def test_multiple_cmd_no_error() -> None:
    """
    Test correct handling of multiple commands succeeding.
    """

    result = CliRunner().invoke(
        exec_cmds_defer_errors,
        ["echo lol", "echo lol"],
    )

    assert "All 2 commands executed successfully." in result.output
    assert "Executed command 1 successfully" in result.output
    assert "Executed command 2 successfully" in result.output

    assert result.exit_code == 0

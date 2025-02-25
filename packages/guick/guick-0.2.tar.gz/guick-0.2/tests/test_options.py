import pytest

import click

from guick import gui


@pytest.mark.parametrize(
    ("args", "expect"),
    [
        ([], "I:[84]"),
        (["--i=23"], "I:[46]"),
        (["--i=x"], "Error: Invalid value for '--i': 'x' is not a valid integer."),
    ],
)
def test_int_option(runner, args, expect):
    @click.command(cls=gui.CommandGui)
    @click.option("--i", default=42)
    def cli(i):
        print(f"I:[{i * 2}]")
        click.echo(f"I:[{i * 2}]")

    result = runner.invoke(cli, args)
    assert expect in result.output

    if expect.startswith("Error:"):
        assert result.exception is not None
    else:
        assert result.exception is None


@pytest.mark.parametrize(
    ("args", "expect"),
    [
        ([], "S:[no value]"),
        (["--s=42"], "S:[42]"),
        (["--s"], "Error: Option '--s' requires an argument."),
        (["--s="], "S:[]"),
        (["--s=\N{SNOWMAN}"], "S:[\N{SNOWMAN}]"),
    ],
)
def test_string_option(runner, args, expect):
    @click.command()
    @click.option("--s", default="no value")
    def cli(s):
        click.echo(f"S:[{s}]")

    result = runner.invoke(cli, args)
    assert expect in result.output

    if expect.startswith("Error:"):
        assert result.exception is not None
    else:
        assert result.exception is None

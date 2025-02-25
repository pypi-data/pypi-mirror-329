import asyncio
from pathlib import Path

import typer

from good_dev.tools.wheelodex import build_dependency_graph
from good_common.utilities import yaml_dump

# from fast_depends import Depends, inject


app = typer.Typer()

# @app.callback()
# def main():
#     typer.echo('main command')


@app.command()
def reverse_dependencies(
    packages: list[str] = typer.Argument(
        ..., help="List of packages to get reverse dependencies for"
    ),
    output: Path = typer.Option(
        "dependencies.yaml", help="Output file to write the dependency graph to"
    ),
):
    typer.echo(f"Getting reverse dependencies for {packages}")

    with asyncio.Runner() as runner:
        dependency_graph = runner.run(build_dependency_graph(packages))

    yaml_dump(output, dependency_graph)


@app.command()
def lookup():
    typer.echo(" command")

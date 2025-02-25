import asyncio
import importlib
import inspect

import typer

from good_common.utilities import parse_args

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main():
    # asyncio.run(broker.connect())
    pass


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def fn(
    ctx: typer.Context,
    command_path: str = typer.Argument(
        ...,
        help="Path to command to run in format module.path.file:function",
    ),
):
    func_args = parse_args(ctx.args)
    module_path, function_name = command_path.split(":")
    module = importlib.import_module(module_path)
    function = getattr(module, function_name)
    # typer.echo(func_args)
    for k, v in func_args.items():
        typer.echo((k, v))

    if inspect.iscoroutinefunction(function):
        with asyncio.Runner() as runner:
            runner.run(function(**func_args))
    else:
        function(**func_args)


@app.command()
def test():
    typer.echo("test command")

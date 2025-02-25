import typer

from . import commands

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main():
    pass


for command in commands.__all__:
    try:
        _app: typer.Typer = getattr(commands, command).app
        if len(getattr(commands, command).app.registered_commands) == 1:
            app.command(command)(
                getattr(commands, command).app.registered_commands[0].callback
            )
        else:
            app.add_typer(getattr(commands, command).app, name=command)
    except AttributeError:
        typer.echo(f"Error: command `{command}` does not have an app attribute")


if __name__ == "__main__":
    app()

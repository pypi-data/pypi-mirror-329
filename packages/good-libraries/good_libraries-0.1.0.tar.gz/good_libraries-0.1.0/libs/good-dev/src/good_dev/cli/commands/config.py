import typer
from loguru import logger

from good_dev.config import settings
from good_common.utilities import deep_attribute_get, deep_attribute_set

# from fast_depends import Depends, inject


app = typer.Typer()


@app.callback(
    no_args_is_help=True,
)
def main(verbose: bool = typer.Option(False, help="Verbose mode.")) -> None:
    _level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(typer.echo, level=_level)


@app.command()
def get(
    key: str = typer.Argument(..., help="Key to get"),
):
    val = deep_attribute_get(settings, key)
    if "secret" in key:
        val = "*" * len(val)
    typer.echo(f"{key}: `{val}`")
    # typer.echo(f'{key}: `{deep_attribute_get(settings, key)}`


@app.command()
def set(
    key: str = typer.Argument(..., help="Key to set"),
    value: str = typer.Argument(..., help="Value to set"),
):
    logger.info(f"Setting {key} to `{value}`")
    deep_attribute_set(settings, key, value)
    settings.update()
    get(key)

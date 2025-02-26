import asyncio

import click
from rich.console import Console

import coiled

from ..utils import CONTEXT_SETTINGS
from .hello import do_hello_wizard


@click.command(context_settings=CONTEXT_SETTINGS)
def hello() -> bool:
    return do_hello_wizard()

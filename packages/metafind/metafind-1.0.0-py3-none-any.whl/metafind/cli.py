from metafind.client import Client
from metafind.clientfactory import get_client
from metafind.errors import MetafindError
from metafind.output import fetch_output

from rich.console import Console
from rich.logging import RichHandler


import sys
import click
import signal
import logging

_SIGINT_EXIT_CODE = 130

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def common_options(func):
    """
    Decorator to attach the same CLI options ('path', 'backend')
    to each command.
    """
    func = click.argument("path", required=True)(func)
    func = click.option(
        "--backend",
        help="Specify a metadata analyzer backend",
        default="exiftool",
        required=True,
    )(func)
    return func


def handle_command(func):
    """
    Decorator to create the backend client and CLI console, as well as handle any exceptions and signals.
    """

    def wrapper(path, backend, *args, **kwargs):
        signal.signal(signal.SIGINT, handle_sigint)
        try:
            client = get_client(backend, path)
            console = Console()
            return func(client, console, *args, **kwargs)
        except MetafindError as e:
            sys.exit(e.error_code)

    # Preserve function metadata (so click doesn't get confused)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_sigint(signum, frame):
    """
    Handler to gracefully exit when sigint is encountered.
    """
    sys.exit(_SIGINT_EXIT_CODE)


@click.group()
def cli():
    """
    Metadata analysis tool created for CSEC-473 - Penetration Testing.

    Authored by sapph2c
    """
    pass


@cli.command(short_help="get file(s) metadata")
@common_options
@handle_command
def fetch(client: Client, console: Console) -> None:
    """
    Retrieves a list of all metadata found within the file(s) at the specified path.
    """
    result = client.get_metadata()
    console.print(fetch_output(result))


@cli.command(short_help="scrub file(s) metadata")
@common_options
@handle_command
def scrub(client: Client, console: Console):
    """
    Attempts to scrub all metadata found within the file(s) at the specified path.
    """
    mutable_tags, immutable_tags = client.scrub_metadata()
    console.print("-------- mutable tags --------")
    console.print(sorted(mutable_tags))
    console.print("-------- immutable tags --------")
    console.print(sorted(immutable_tags))


@cli.command(short_help="get unique tags from file(s)")
@common_options
@handle_command
def unique(client: Client, console: Console) -> None:
    """
    Gets an alphabetized list of all unique metadata tags found within the file(s) at the specified path.
    """
    result = client.get_unique_tags()
    console.print(sorted(result))

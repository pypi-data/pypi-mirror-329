import click
from askoclics.cli.commands.dataset.delete import cli as delete
from askoclics.cli.commands.dataset.list import cli as list
from askoclics.cli.commands.dataset.set_public import cli as set_public
from askoclics.cli.commands.dataset.set_private import cli as set_private


@click.group()
def cli():
    """
    Manipulate datasets managed by Askomics
    """
    pass


cli.add_command(delete)
cli.add_command(list)
cli.add_command(set_public)
cli.add_command(set_private)

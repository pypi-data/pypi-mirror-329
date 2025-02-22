import click
from askoclics.cli.commands.result.delete import cli as delete
from askoclics.cli.commands.result.download import cli as download
from askoclics.cli.commands.result.get_sparql import cli as get_sparql
from askoclics.cli.commands.result.list import cli as list
from askoclics.cli.commands.result.preview import cli as preview


@click.group()
def cli():
    """
    Interact with AskOmics results
    """
    pass


cli.add_command(delete)
cli.add_command(download)
cli.add_command(get_sparql)
cli.add_command(list)
cli.add_command(preview)

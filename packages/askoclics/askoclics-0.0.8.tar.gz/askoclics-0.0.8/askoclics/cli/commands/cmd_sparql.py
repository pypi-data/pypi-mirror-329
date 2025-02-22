import click
from askoclics.cli.commands.sparql.info import cli as info
from askoclics.cli.commands.sparql.query import cli as query
from askoclics.cli.commands.sparql.template import cli as template


@click.group()
def cli():
    """
    Send SPARQL queries to Askomics
    """
    pass


cli.add_command(info)
cli.add_command(query)
cli.add_command(template)

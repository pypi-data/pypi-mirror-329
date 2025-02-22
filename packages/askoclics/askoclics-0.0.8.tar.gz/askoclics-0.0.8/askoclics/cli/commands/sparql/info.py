import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('info')
@pass_context
@custom_exception
@dict_output
def cli(ctx):
    """Return available graphs, endpoints, and uris

Output:

    Dict with info
    """
    return ctx.gi.sparql.info()

import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('list')
@pass_context
@custom_exception
@dict_output
def cli(ctx):
    """List results

Output:

    Dict with info
    """
    return ctx.gi.result.list()

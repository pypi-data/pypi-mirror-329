import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('get_sparql')
@click.argument("result_id", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, result_id):
    """Show results preview

Output:

    Dict with info
    """
    return ctx.gi.result.get_sparql(result_id)

import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, None_output


@click.command('delete')
@click.argument("result_ids", type=str)
@pass_context
@custom_exception
@None_output
def cli(ctx, result_ids):
    """Delete results

Output:

    None
    """
    return ctx.gi.result.delete(result_ids)

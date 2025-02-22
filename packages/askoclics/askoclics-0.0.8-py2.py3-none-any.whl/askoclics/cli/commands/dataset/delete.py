import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, list_output


@click.command('delete')
@click.argument("datasets", type=str)
@pass_context
@custom_exception
@list_output
def cli(ctx, datasets):
    """Send a delete task on a list of datasets

Output:

    List of the datasets
    """
    return ctx.gi.dataset.delete(datasets)

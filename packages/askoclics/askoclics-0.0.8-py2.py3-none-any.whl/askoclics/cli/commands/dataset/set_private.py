import click
from askoclics.cli.cli import pass_context
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('set_private')
@click.argument("dataset_id", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, dataset_id):
    """Privatize a dataset

Output:

    Dictionary with info and datasets
    """
    return ctx.gi.dataset.set_private(dataset_id)

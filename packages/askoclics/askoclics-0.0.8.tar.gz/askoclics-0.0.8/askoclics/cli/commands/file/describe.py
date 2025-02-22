import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, list_output


@click.command('describe')
@click.argument("files", type=str)
@pass_context
@custom_exception
@list_output
def cli(ctx, files):
    """Show file information

Output:

    List of files containing info
    """
    return ctx.gi.file.describe(files)

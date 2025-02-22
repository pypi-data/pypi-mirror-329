import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('preview')
@click.argument("files", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, files):
    """Get preview for a list of files

Output:

    Dictionary containing the information
    """
    return ctx.gi.file.preview(files)

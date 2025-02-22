import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('upload')
@click.option(
    "--url",
    help="URL to the file",
    type=str
)
@click.option(
    "--file_path",
    help="Path to the file to upload",
    type=str
)
@click.option(
    "--verbose",
    help="Show progression bar for local file upload",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, url="", file_path="", verbose=False):
    """Upload a file to AskOmics

Output:

    Dict with results
    """
    return ctx.gi.file.upload(url=url, file_path=file_path, verbose=verbose)

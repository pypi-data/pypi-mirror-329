import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('integrate_rdf')
@click.argument("file_id", type=str)
@click.option(
    "--external_endpoint",
    help="External endpoint",
    type=str
)
@click.option(
    "--skip_preview",
    help="Skip the preview step for big files",
    is_flag=True
)
@click.option(
    "--public",
    help="Set the generated dataset as public (admin only)",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id, external_endpoint="", skip_preview=False, public=False):
    """Send an integration task for a specified file_id

Output:

    Dictionary of task information
    """
    return ctx.gi.file.integrate_rdf(file_id, external_endpoint=external_endpoint, skip_preview=skip_preview, public=public)

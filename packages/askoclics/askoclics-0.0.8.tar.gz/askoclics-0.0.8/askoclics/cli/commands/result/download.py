import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, None_output


@click.command('download')
@click.argument("result_id", type=str)
@click.argument("file_path", type=str)
@pass_context
@custom_exception
@None_output
def cli(ctx, result_id, file_path):
    """Download a result to a file

Output:

    None
    """
    return ctx.gi.result.download(result_id, file_path)

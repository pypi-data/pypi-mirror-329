import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, None_output


@click.command('template')
@click.argument("file_path", type=str)
@pass_context
@custom_exception
@None_output
def cli(ctx, file_path):
    """Write the default query to a file

Output:

    None
    """
    return ctx.gi.sparql.template(file_path)

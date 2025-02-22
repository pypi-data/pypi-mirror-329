import click
from askoclics.cli.cli import pass_context, json_loads
from askoclics.cli.decorators import custom_exception, dict_output


@click.command('query')
@click.argument("query", type=str)
@click.argument("graphs", type=str)
@click.argument("endpoints", type=str)
@click.option(
    "--full_query",
    help="Whether to send a full query or a preview",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, query, graphs, endpoints, full_query=False):
    """Send a SPARQL query

Output:

    The API call result (either the result id, or the result preview)
    """
    return ctx.gi.sparql.query(query, graphs, endpoints, full_query=full_query)

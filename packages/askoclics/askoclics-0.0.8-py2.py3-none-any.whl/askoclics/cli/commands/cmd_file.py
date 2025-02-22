import click
from askoclics.cli.commands.file.delete import cli as delete
from askoclics.cli.commands.file.describe import cli as describe
from askoclics.cli.commands.file.integrate_bed import cli as integrate_bed
from askoclics.cli.commands.file.integrate_csv import cli as integrate_csv
from askoclics.cli.commands.file.integrate_gff import cli as integrate_gff
from askoclics.cli.commands.file.integrate_rdf import cli as integrate_rdf
from askoclics.cli.commands.file.list import cli as list
from askoclics.cli.commands.file.preview import cli as preview
from askoclics.cli.commands.file.upload import cli as upload


@click.group()
def cli():
    """
    Manipulate files managed by AskOmics
    """
    pass


cli.add_command(delete)
cli.add_command(describe)
cli.add_command(integrate_bed)
cli.add_command(integrate_csv)
cli.add_command(integrate_gff)
cli.add_command(integrate_rdf)
cli.add_command(list)
cli.add_command(preview)
cli.add_command(upload)

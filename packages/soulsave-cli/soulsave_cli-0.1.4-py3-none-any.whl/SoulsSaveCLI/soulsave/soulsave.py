import click
from SoulsSaveCLI.soulsave import core


@click.group()
def cli():
    pass

cli.add_command(core.new)
cli.add_command(core.add)
cli.add_command(core.load)
cli.add_command(core.list)
cli.add_command(core.init)
cli.add_command(core.rm)

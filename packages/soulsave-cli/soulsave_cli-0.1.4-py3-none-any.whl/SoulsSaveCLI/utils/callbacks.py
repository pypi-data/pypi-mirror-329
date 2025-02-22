import click
import os
import shutil
from SoulsSaveCLI.utils import side_functions


def load_last(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    config_data = side_functions.get_data('config.yaml')

    last_load = config_data[3]
    last_dest = config_data[0] + config_data[1]

    if os.path.isfile(last_load):
        shutil.copyfile(last_load, last_dest)
        click.echo(f"Successfully loaded '{last_load}'")

    else:
        click.echo(f"'{last_load}' does not exist. Use `soulsave list` for a list of available options.")

    ctx.exit()

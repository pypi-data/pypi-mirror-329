import click
from axcli import read, load, catalog, run, show, live
from axcli.menu import menu
from axcli._list import _list

@click.group()
def cli():
    pass

cli.add_command(read)
cli.add_command(load)
cli.add_command(catalog)
cli.add_command(run)
cli.add_command(show)
cli.add_command(live)
cli.add_command(menu)
cli.add_command(_list)

def main():
    cli()
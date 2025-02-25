import os, click
from colorama import Fore, Style

@click.command(name="list")
@click.argument("path", default=".")
def _list(path):
    "Lists the .ax files in the current directory."
    ax_files = [f for f in os.listdir(path) if f.endswith('.ax')]
    print(f"There are {Fore.RED}{len(ax_files)}{Style.RESET_ALL} .ax files:")
    for f in ax_files:
        if f.endswith('.tmpl.ax'):
            print(f"  - {Fore.MAGENTA}{f}{Style.RESET_ALL}")
        else:
            print(f"  - {Fore.RED}{f}{Style.RESET_ALL}")
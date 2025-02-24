import axinite.tools as axtools
import click

@click.command("live")
@click.argument("path", type=click.Path(exists=True))
@click.option("-f", "--frontend", type=str, default="vpython")
@click.option("-s", type=int, default=1)
@click.option("-r", "--rate", type=int, default=-1)
def live(path, frontend, s, rate):
    "Watch a system live."
    name_to_frontend = {
        "vpython": axtools.vpython_frontend,
        "mpl": axtools.mpl_frontend,
    }
    args = axtools.read(path)
    if rate != -1: args["rate"] = rate
    axtools.live(args, name_to_frontend[frontend](args, "live", s=s))
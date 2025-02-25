import axinite.tools as axtools
import axinite as ax
import click

@click.command("show")
@click.argument("path", type=click.Path(exists=True))
@click.option("-f", "--frontend", type=str, default="plotly")
def show(path, frontend):
    "Show a system as a static display."
    name_to_frontend = {
        "vpython": axtools.vpython_frontend,
        "plotly": axtools.plotly_frontend,
        "mpl": axtools.mpl_frontend,
        "mpl-3d": lambda args, type: axtools.mpl_frontend(args, type, "3D"),
    }
    args = axtools.read(path)
    axtools.show(args, name_to_frontend[frontend](args, "show"))
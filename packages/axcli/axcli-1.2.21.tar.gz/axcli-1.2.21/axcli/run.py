import axinite.tools as axtools
import axinite as ax
import click

@click.command("run")
@click.argument("path", type=click.Path(exists=True))
@click.option("-b", "--backend", type=str, default="verlet")
@click.option("-f", "--frontend", type=str, default="vpython")
def run(path, backend, frontend):
    "Watch and load a system simultaneously."
    name_to_backend = {
        "verlet": ax.verlet_backend,
        "euler": ax.euler_backend,
    }
    name_to_frontend = {
        "vpython": axtools.vpython_frontend,
        "mpl": axtools.mpl_frontend,
    }
    args = axtools.read(path)
    args.backend = name_to_backend[backend]
    axtools.run(args, name_to_frontend[frontend](args, "run"))
import click, os, axinite as ax
import axinite.tools as axtools

name_to_backend = {
    "verlet": ax.verlet_backend,
    "euler": ax.euler_backend,
    "rk2": ax.rk2_backend,
    "rk3": ax.rk3_backend,
    "rk4": ax.rk4_backend,
}

@click.command("load")
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("output_path", type=click.Path(exists=False, file_okay=True, dir_okay=True), default="")
@click.option("-l", "--limit", default="-1")
@click.option("-d", "--delta", default="-1")
@click.option("-b", "--backend", type=str, default="verlet")
def load(input_path, output_path, limit, delta, backend):
    "Load a system from a file."
    print("Preparing...", end='\r')
    args = axtools.read(input_path)
    args.backend = name_to_backend[backend]
    if delta != "-1": args.set_delta(ax.interpret_time(delta))
    if limit != "-1": args.set_limit(ax.round_limit(ax.interpret_time(limit), args.delta))
    if output_path != "":
        if os.path.isdir(output_path): axtools.load(args, f"{output_path}/{args.name}.ax", verbose=True) 
        else: axtools.load(args, output_path, verbose=True)
    else: axtools.load(args, f"{args.name}.ax", verbose=True)
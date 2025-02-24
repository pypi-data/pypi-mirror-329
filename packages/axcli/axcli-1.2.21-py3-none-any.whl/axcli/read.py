import click, json

@click.command("read")
@click.argument("path", type=click.Path(exists=True))
def read(path):
    "Read a system from a file."
    with open(path, "r") as file:
        system = json.load(file)
        
        click.echo(f"Name: {system['name']}")
        click.echo(f"Author: {system['author'] or 'Unknown'}")
        click.echo(f"Limit: {system['limit']}")
        click.echo(f"Delta: {system['delta']}")
        click.echo(f"Framerate: {system['rate'] or 'Unknown'}")
        click.echo("Bodies:")
        for body in system['bodies']:
            position = f"({body['r']['x']}, {body['r']['y']}, {body['r']['z']}) m"
            velocity = f"({body['v']['x']}, {body['v']['y']}, {body['v']['z']}) m/s"
            click.echo(f"  {body['name']} - {body['mass']} kg {position} at {velocity}")
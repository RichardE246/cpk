import cpk.utils as utils
import click
from pathlib import Path

@click.group()
def cli():
    pass

@cli.command()
def activate():
    utils.activate()

@cli.command()
@click.argument('url')
def install(url):
    utils.install(url)

@cli.command()
@click.argument('name')
def uninstall(name):
    utils.uninstall(name)

@cli.command()
@click.argument('path')
def init(path):
    utils.init(path)

@cli.command()
def build():
    print(Path.cwd())
    utils.build(Path("."))

if __name__ == '__main__':
    cli()

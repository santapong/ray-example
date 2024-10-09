import click
import requests

@click.command()
@click.option('--name', default='Hello', help='test')
def cli(name):
    click.echo(f'{name}')

if __name__ == '__main__':
    cli()

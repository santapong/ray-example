from selectors import SelectSelector
import click
import requests

from core.utils import SessionDB
from core.utils import appilcationGen

from dotenv import load_dotenv

load_dotenv()

import os

@click.group()
def cli():
    """ This is the main CLI Group. """
    pass

@cli.add_command
@click.command()
def init():
    """
    Use for init connect to database
    """
    
    session = SessionDB()
    session.create_table()

@cli.add_command
@click.command()
def deploy():
    """
    Use for Deploy Application in Database
    """
    session = SessionDB()

    appilcations = appilcationGen(session=session)
    click.echo(appilcations)


if __name__ == '__main__':
    cli()

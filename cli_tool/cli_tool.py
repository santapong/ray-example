import click
import requests

from core.utils.session import SessionDB

from dotenv import load_dotenv
load_dotenv()

import os

@click.group()
def cli():
    """ This is the main CLI Group. """
    pass

@cli.add_command
@click.command(name= "-i" ,help = "Use for init connect to database")
def init():
    session = SessionDB()
    session.create_table()




if __name__ == '__main__':
    cli()

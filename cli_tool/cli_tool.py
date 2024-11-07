import click
import requests
import json
import os

from core.utils.requestTemplate import Template, HEADERS, RAY_DEPLOY_URL

from core.utils import SessionDB
from core.utils import appilcationGen

from dotenv import load_dotenv

load_dotenv()



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

    applications = appilcationGen(session=session)

    Template['applications'] = applications
    json_template = json.dumps(Template, indent=4)

    requests.put(url=RAY_DEPLOY_URL, data=json_template, headers=HEADERS)

    click.echo(json_template)


if __name__ == '__main__':
    cli()

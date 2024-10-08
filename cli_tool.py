import click
import requests

@click.command()
@click.argument('endpoint')
@click.option('--method', default='GET', help='HTTP method to use (GET, POST, etc.)')
@click.option('--data', default=None, help='Data to send with the request (for POST requests)')
def cli(endpoint, method, data):
    """CLI tool to make API requests."""
    url = f'https://jsonplaceholder.typicode.com/{endpoint}'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data)
        else:
            click.echo(f"Unsupported method: {method}")
            return

        click.echo(f"Response Code: {response.status_code}")
        click.echo("Response Body:")
        click.echo(response.json())
    except requests.exceptions.RequestException as e:
        click.echo(f"An error occurred: {e}")

if __name__ == '__main__':
    cli()

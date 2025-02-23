import click
from ..utils import print_json

@click.group()
def environments():
    """Manage environments"""
    pass

@environments.command('list')
@click.pass_obj
def list_environments(client):
    """List all environments"""
    with client as c:
        res = c.environments.get()
        print_json(res.model_dump()) 
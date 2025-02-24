import click
from ..utils import print_json

@click.group()
def compute():
    """Manage compute resources"""
    pass

@compute.command('list')
@click.pass_obj
def list_compute(client):
    """List compute information"""
    with client as c:
        res = c.compute.get()
        print_json(res.model_dump()) 
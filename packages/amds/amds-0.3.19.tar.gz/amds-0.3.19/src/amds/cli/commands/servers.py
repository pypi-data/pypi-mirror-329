import click
from ..utils import print_json

@click.group()
def servers():
    """Manage servers"""
    pass

@servers.command('list')
@click.pass_obj
def list_servers(client):
    """List all servers"""
    with client as c:
        res = c.servers.get()
        print_json(res.model_dump())

@servers.command('get')
@click.option('--server-id', required=True, help='ID of the server')
@click.pass_obj
def get_server(client, server_id):
    """Get server information"""
    with client as c:
        res = c.servers.get(server_id=server_id)
        print_json(res.model_dump())

@servers.command('start')
@click.option('--server-id', required=True, help='ID of the server')
@click.pass_obj
def start_server(client, server_id):
    """Start a server"""
    with client as c:
        res = c.servers.start(server_id=server_id)
        print_json(res.model_dump())

@servers.command('stop')
@click.option('--server-id', required=True, help='ID of the server')
@click.pass_obj
def stop_server(client, server_id):
    """Stop a server"""
    with client as c:
        res = c.servers.stop(server_id=server_id)
        print_json(res.model_dump())

@servers.command('delete')
@click.option('--server-id', required=True, help='ID of the server')
@click.pass_obj
def delete_server(client, server_id):
    """Delete a server"""
    with client as c:
        res = c.servers.delete(server_id=server_id)
        print_json(res.model_dump())

@servers.command('upload-file')
@click.option('--server-id', required=True, help='ID of the server')
@click.option('--local-path', required=True, type=click.Path(exists=True), help='Local file path')
@click.option('--remote-path', required=True, help='Remote file path')
@click.pass_obj
def upload_file(client, server_id, local_path, remote_path):
    """Upload a file to a server"""
    with client as c:
        with open(local_path, 'rb') as f:
            res = c.servers.upload_file(
                server_id=server_id,
                file=f,
                path=remote_path
            )
            print_json(res.model_dump())

@servers.command('run-code')
@click.option('--server-id', required=True, help='ID of the server')
@click.option('--code', required=True, help='Python code to execute')
@click.pass_obj
def run_code(client, server_id, code):
    """Run code on a server"""
    with client as c:
        res = c.servers.run_code(
            server_id=server_id,
            code=code
        )
        print_json(res.model_dump()) 
import click
from ..utils import print_json


@click.group()
def servers():
    """Manage servers"""
    pass


@servers.command("list")
@click.pass_obj
def list_servers(client):
    """List all servers"""
    with client as c:
        res = c.servers.get()
        print_json(res.model_dump())


@servers.command("get")
@click.option("--server-name", required=True, help="Name of the server")
@click.pass_obj
def get_server(client, server_name):
    """Get server information"""
    with client as c:
        res = c.servers.get(server_name=server_name)
        print_json(res.model_dump())


@servers.command("create")
@click.option("--name", required=True, help="Name of the server")
@click.option("--environment", default="ai", help="Server environment")
@click.option("--port", type=int, default=5000, help="Server port")
@click.option("--server-type", default="amds-medium_cpu", help="Server type/request")
@click.pass_obj
def create_server(client, name, environment, port, server_type):
    """Create a server"""
    with client as c:
        res = c.servers.create(
            request={
                "environment": environment,
                "port": port,
                "server_name": name,
                "server_request": server_type,
            }
        )
        print_json(res.model_dump())


@servers.command("stop")
@click.option("--server-name", required=True, help="Name of the server")
@click.pass_obj
def stop_server(client, server_name):
    """Stop a server"""
    with client as c:
        res = c.servers.stop(server_name=server_name)
        click.echo(f"✓ Server '{server_name}' stopped successfully")


@servers.command("start")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--environment", required=False, default="ai", help="Server environment")
@click.option("--port", type=int, required=False, default=5000, help="Server port")
@click.option("--server-type", required=False, default="amds-medium_cpu", help="Server type")
@click.pass_obj
def start_server(client, server_name, environment, port, server_type):
    """Start a server"""
    with client as c:
        res = c.servers.start(
            server_name=server_name,
            environment=environment,
            port=port,
            server_request=server_type,
        )
        click.echo(f"\n✓ Server '{server_name}' started successfully")
        if res.port_forward_url:
            click.echo(f"\nAccess your server at:")
            click.echo(click.style(f"  {res.port_forward_url}", fg="bright_blue"))
        if res.hourly_rate:
            click.echo(f"\nHourly rate: ${res.hourly_rate:.2f}")


@servers.command("delete")
@click.option("--server-name", required=True, help="Name of the server")
@click.pass_obj
def delete_server(client, server_name):
    """Delete a server"""
    with client as c:
        res = c.servers.delete(server_name=server_name)
        print_json(res.model_dump())


@servers.command("get-file")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--path", required=True, help="Remote file path")
@click.pass_obj
def get_file(client, server_name, path):
    """Get a file from a server"""
    with client as c:
        res = c.servers.get_file(server_name=server_name, path=path)
        print_json(res.model_dump())


@servers.command("upload-file")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--path", required=True, help="Remote file path")
@click.option("--content", help="File content")
@click.option("--format", "format_", default="text", help="File format")
@click.option("--type", "type_", default="file", help="Content type")
@click.pass_obj
def upload_file(client, server_name, path, content, format_, type_):
    """Upload a file to a server"""
    with client as c:
        res = c.servers.upload_file(
            server_name=server_name,
            path=path,
            content=content,
            format_=format_,
            type_=type_,
        )
        print_json(res.model_dump())


@servers.command("run-code")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--code", help="Python code to execute")
@click.option("--kernel-name", default="api-kernel", help="Kernel name")
@click.pass_obj
def run_code(client, server_name, code, kernel_name):
    """Run code on a server"""
    with client as c:
        res = c.servers.run_code(
            server_name=server_name, code=code, kernel_name=kernel_name
        )
        print_json(res.model_dump())

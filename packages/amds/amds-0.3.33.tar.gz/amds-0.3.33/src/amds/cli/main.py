import click
import sys
import os
import json
from amds import Amds
from .commands import environments, servers, compute, alph, login
from .commands.login import get_config_path, is_token_valid


@click.group()
@click.option("--api-key", envvar="AMDS_API_KEY", help="API key for authentication")
@click.pass_context
def cli(ctx: click.Context, api_key: str):
    """American Data Science CLI - Command line interface for the American Data Science API"""
    
    # Skip API key check for login command
    if ctx.invoked_subcommand == 'login':
        ctx.obj = None
        return

    # If no API key provided via env or flag, try to get from config
    if not api_key:
        try:
            config_path = get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if is_token_valid(config):
                        api_key = config.get('auth_token')
        except Exception:
            pass

    if not api_key:
        click.echo(
            "Error: API key is required. Either:\n\n"
            "    1. Run 'amds login' to authenticate via browser\n"
            "    2. Set AMDS_API_KEY environment variable\n"
            "    3. Use --api-key option",
            err=True,
        )
        sys.exit(1)
    ctx.obj = Amds(api_key=api_key)


cli.add_command(environments.environments)
cli.add_command(servers.servers)
cli.add_command(compute.compute)
cli.add_command(alph.alph)
cli.add_command(login.login)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()

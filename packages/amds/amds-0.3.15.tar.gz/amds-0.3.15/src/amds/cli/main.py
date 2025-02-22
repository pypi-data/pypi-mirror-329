import click
import sys
from amds import Amds
from .commands import environments, servers, compute, alph


@click.group()
@click.option("--api-key", envvar="AMDS_API_KEY", help="API key for authentication")
@click.pass_context
def cli(ctx: click.Context, api_key: str):
    """American Data Science CLI - Command line interface for the American Data Science API"""
    if not api_key:
        click.echo(
            "Error: API key is required. Set AMDS_API_KEY environment variable or use --api-key option",
            err=True,
        )
        sys.exit(1)
    ctx.obj = Amds(api_key=api_key)


cli.add_command(environments.environments)
cli.add_command(servers.servers)
cli.add_command(compute.compute)
cli.add_command(alph.alph)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()

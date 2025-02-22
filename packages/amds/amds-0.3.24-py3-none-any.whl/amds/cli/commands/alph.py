import click
import sys
import json
from ..utils import print_json


@click.group()
def alph():
    """AI language model operations"""
    pass


@alph.command("gpt4o-mini")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--message", required=True, help="Message to send to the model")
@click.pass_obj
def gpt4o_mini(client, server_name, message):
    """Use gpt-4o-mini model"""
    with client as c:
        res = c.alph.gpt4o_mini(
            server_name=server_name, messages=[{"content": message, "role": "user"}]
        )

        if hasattr(res, "text"):
            sys.stdout.write(res.text)
            sys.stdout.write("\n")
        else:
            print_json(res.model_dump())


@alph.command("gpt4o")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--message", required=True, help="Message to send to the model")
@click.pass_obj
def gpt4o(client, server_name, message):
    """Use gpt-4o model"""
    with client as c:
        res = c.alph.gpt4o(
            server_name=server_name, messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, "text"):
            sys.stdout.write(res.text)
            sys.stdout.write("\n")
        else:
            print_json(res.model_dump())


@alph.command("gpt4")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--message", required=True, help="Message to send to the model")
@click.pass_obj
def gpt4(client, server_name, message):
    """Use gpt-4 model"""
    with client as c:
        res = c.alph.gpt4(
            server_name=server_name, messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, "text"):
            sys.stdout.write(res.text)
            sys.stdout.write("\n")
        else:
            print_json(res.model_dump())


@alph.command("claude35-haiku")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--message", required=True, help="Message to send to the model")
@click.pass_obj
def claude35_haiku(client, server_name, message):
    """Use claude-3.5-haiku model"""
    with client as c:
        res = c.alph.claude35_haiku(
            server_name=server_name, messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, "text"):
            sys.stdout.write(res.text)
            sys.stdout.write("\n")
        else:
            print_json(res.model_dump())


@alph.command("claude35-sonnet")
@click.option("--server-name", required=True, help="Name of the server")
@click.option("--message", required=True, help="Message to send to the model")
@click.pass_obj
def claude35_sonnet(client, server_name, message):
    """Use claude-3.5-sonnet model"""
    with client as c:
        res = c.alph.claude35_sonnet(
            server_name=server_name, messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, "text"):
            sys.stdout.write(res.text)
            sys.stdout.write("\n")
        else:
            print_json(res.model_dump())

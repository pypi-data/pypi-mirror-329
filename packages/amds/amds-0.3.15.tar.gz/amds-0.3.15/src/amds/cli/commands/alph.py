import click
import sys
import json
from ..utils import print_json

@click.group()
def alph():
    """AI language model operations"""
    pass

@alph.command('gpt4o-mini')
@click.option('--server-name', required=True, help='Name of the server')
@click.option('--message', required=True, help='Message to send to the model')
@click.pass_obj
def gpt4o_mini(client, server_name, message):
    """Use gpt-4o-mini model"""
    with client as c:
        res = c.alph.gpt4o_mini(
            server_name=server_name,
            messages=[{"content": message, "role": "user"}]
        )
        
        # Access the raw response object
        raw_response = res.raw_response
        if raw_response.encoding is None:
            raw_response.encoding = 'utf-8'

        full_output = []
        try:
            for line in raw_response.iter_lines(decode_unicode=True):
                if line:
                    split_line = line.split(':', 1)
                    try:
                        tool_call = json.loads(split_line[1])
                        cleaned_line = json.dumps(tool_call.get('result', ''), indent=4)
                        sys.stdout.write('\nAnalyzing...\n')
                        sys.stdout.write(cleaned_line)
                    except:
                        cleaned_line = split_line[1].replace('"', '')
                        if r'\n' in cleaned_line:
                            sys.stdout.write(cleaned_line.replace(r'\n', ''))
                        else:
                            sys.stdout.write(cleaned_line)
                    full_output.append(cleaned_line)
            sys.stdout.write('\n')
        except ValueError:
            sys.stdout.write('Response encoded incorrectly.\n')
            if hasattr(res, 'text'):
                sys.stdout.write(res.text)
                sys.stdout.write('\n')
            else:
                print_json(res.model_dump())

@alph.command('gpt4o')
@click.option('--server-name', required=True, help='Name of the server')
@click.option('--message', required=True, help='Message to send to the model')
@click.pass_obj
def gpt4o(client, server_name, message):
    """Use gpt-4o model"""
    with client as c:
        res = c.alph.gpt4o(
            server_name=server_name,
            messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, 'text'):
            sys.stdout.write(res.text)
            sys.stdout.write('\n')
        else:
            print_json(res.model_dump())

@alph.command('gpt4')
@click.option('--server-name', required=True, help='Name of the server')
@click.option('--message', required=True, help='Message to send to the model')
@click.pass_obj
def gpt4(client, server_name, message):
    """Use gpt-4 model"""
    with client as c:
        res = c.alph.gpt4(
            server_name=server_name,
            messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, 'text'):
            sys.stdout.write(res.text)
            sys.stdout.write('\n')
        else:
            print_json(res.model_dump())

@alph.command('claude35-haiku')
@click.option('--server-name', required=True, help='Name of the server')
@click.option('--message', required=True, help='Message to send to the model')
@click.pass_obj
def claude35_haiku(client, server_name, message):
    """Use claude-3.5-haiku model"""
    with client as c:
        res = c.alph.claude35_haiku(
            server_name=server_name,
            messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, 'text'):
            sys.stdout.write(res.text)
            sys.stdout.write('\n')
        else:
            print_json(res.model_dump())

@alph.command('claude35-sonnet')
@click.option('--server-name', required=True, help='Name of the server')
@click.option('--message', required=True, help='Message to send to the model')
@click.pass_obj
def claude35_sonnet(client, server_name, message):
    """Use claude-3.5-sonnet model"""
    with client as c:
        res = c.alph.claude35_sonnet(
            server_name=server_name,
            messages=[{"content": message, "role": "user"}]
        )
        if hasattr(res, 'text'):
            sys.stdout.write(res.text)
            sys.stdout.write('\n')
        else:
            print_json(res.model_dump())

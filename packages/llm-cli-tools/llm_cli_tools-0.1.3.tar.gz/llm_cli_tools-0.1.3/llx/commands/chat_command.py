import asyncio
import click
from abc import ABC
from llx.utils import get_provider

class ChatCommand(ABC):
    """Handle the interactive chat command logic"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.client = get_provider(provider, model)

    async def _print_stream(self, stream):
        click.echo(click.style("Assistant: ", fg='green'), nl=False)
        async for chunk in stream:
            click.echo(click.style(chunk, fg='green'), nl=False)
        click.echo()

    def execute(self):
        click.echo(f"Starting interactive shell with model {self.model}")
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ['/bye']:
                    click.echo("Bye.")
                    break
                
                stream = self.client.invoke(user_input)
                asyncio.run(self._print_stream(stream))
            except (EOFError, KeyboardInterrupt):
                click.echo("\nBye.")
                break

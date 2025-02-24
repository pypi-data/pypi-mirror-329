import click
from dotenv import load_dotenv
from typing import Optional
from llx.commands.chat_command import ChatCommand
from llx.commands.prompt_command import PromptCommand
from llx.commands.server_command import ServerCommand
from llx.commands.url_to_prompt_command import UrlToPromptCommand
from llx.commands.files_to_prompt_command import FilesToPromptCommand

@click.group()
def llx():
    """CLI tool to interact with various LLM APIs."""
    pass

@llx.command()
@click.option('--model', '-m', required=True, help='The model to use for the LLM API in the format <provider>:<model>.')
@click.option('--prompt', '-p', required=False)
@click.option('--attachment', '-a', required=False, type=click.Path(exists=True), help='Path to an attachment file.')
def prompt(model: str, prompt: Optional[str], attachment: Optional[str]):
    """Invoke the target LLM and model with the specified prompt."""
    provider, model_name = model.split(':', 1)
    command = PromptCommand(provider, model_name)
    command.execute(prompt, attachment)

@llx.command()
@click.option('--host', required=True, help='The host to start the server on.', default='127.0.0.1')
@click.option('--port', required=True, type=int, help='The port to start the server on.', default=8000)
def server(host: str, port: int):
    """Start a server."""
    command = ServerCommand()
    command.execute(host, port)

@llx.command()
@click.option('--model', '-m', required=True, help='The model to use for the LLM API in the format <provider>:<model>.')
def chat(model: str):
    """Start an interactive shell with the target LLM."""
    provider, model_name = model.split(':', 1)
    command = ChatCommand(provider, model_name)
    command.execute()

@llx.command()
@click.option('--url', required=True, help='The URL to extract content from.')
@click.option('--prompt', '-p', required=False, help='The prompt to prepend.')
@click.option('--extract-text', required=False, type=bool, default=False, help='If true extract text from the HTML content.')
@click.option('--domain', required=False, help='The domain to restrict crawling to.')
@click.option('--max-depth', required=False, type=int, default=1, help='The depth to crawl.')
@click.option('--max-urls', required=False, type=int, default=1, help='The maximum number of URLs to crawl.')
def url_to_prompt(url: str, prompt: Optional[str], extract_text: bool,
                 domain: Optional[str], max_depth: int, max_urls: int):
    """Extract content from a URL and prepend as context to the LLM prompt."""
    command = UrlToPromptCommand()
    command.execute(url, prompt, extract_text, domain, max_depth, max_urls)

@llx.command()
@click.option('--path', required=True, type=click.Path(exists=True), help='The path to concatenate files from.')
@click.option('--prompt', '-p', required=False, help='The prompt to prepend.')
def files_to_prompt(path: str, prompt: Optional[str]):
    """Concatenate all files in the given path. Prepend the prompt to the text if provided."""
    command = FilesToPromptCommand()
    command.execute(path, prompt)

def main():
    load_dotenv()
    llx()

if __name__ == '__main__':
    main()
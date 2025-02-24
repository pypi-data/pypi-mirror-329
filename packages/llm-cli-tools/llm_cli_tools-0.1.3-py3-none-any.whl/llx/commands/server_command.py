import click
import uvicorn
from llx.server import app
from abc import ABC

class ServerCommand(ABC):
    """Handle the server command logic"""
    
    def execute(self, host: str = '127.0.0.1', port: int = 8000):
        click.echo(f"Starting server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)

import os
import mimetypes
from typing import Optional
import click
from abc import ABC

class FilesToPromptCommand(ABC):
    """Handle file concatenation and prompt generation"""
    
    def execute(self, path: str, prompt: Optional[str]):
        if not os.path.isdir(path):
            raise click.ClickException(f"The path {path} is not a directory.")

        concatenated_text = self._concatenate_files(path)
        full_prompt = f"{prompt}\n\n{concatenated_text}" if prompt else concatenated_text
        click.echo(full_prompt)

    def _concatenate_files(self, path: str) -> str:
        concatenated_text = "<documents>\n"
        for root, _, files in os.walk(path):
            for index, file in enumerate(files, start=1):
                file_path = os.path.join(root, file)
                if self._is_binary_file(file_path):
                    continue
                try:
                    concatenated_text += self._process_file(file_path, file, index)
                except UnicodeDecodeError:
                    pass
        concatenated_text += "</documents>"
        return concatenated_text

    def _process_file(self, file_path: str, file: str, index: int) -> str:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
            return (f"  <document index=\"{index}\">\n"
                   f"    <source>{file}</source>\n"
                   f"    <document_content>\n"
                   f"      {file_content}\n"
                   f"    </document>\n")

    def _is_binary_file(self, filepath: str) -> bool:
        mime = mimetypes.guess_type(filepath)[0]
        return mime is not None and mime.startswith('application/')

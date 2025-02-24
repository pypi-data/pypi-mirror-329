import pytest
from click.testing import CliRunner
import sys
sys.path.insert(0, '/Users/marcocampana/code/llx')  # Ensure the project directory is included in the path
from llx.cli import llx

@pytest.fixture
def runner():
    return CliRunner()

def test_prompt_with_argument(runner, mocker):
    mock_fetch_api_response = mocker.patch('llx.cli.fetch_api_response', return_value=["response chunk"])
    result = runner.invoke(llx, ['prompt', '--target', 'openai', '--model', 'gpt4o', '--prompt', 'Hello'])
    assert result.exit_code == 0
    mock_fetch_api_response.assert_called_once_with('openai', 'gpt4o', 'Hello', None)
    assert "response chunk" in result.output

def test_prompt_with_stdin(runner, mocker):
    mock_fetch_api_response = mocker.patch('llx.cli.fetch_api_response', return_value=["response chunk"])
    result = runner.invoke(llx, ['prompt', '--target', 'openai', '--model', 'text-davinci-003'], input='Hello from stdin')
    assert result.exit_code == 0
    mock_fetch_api_response.assert_called_once_with('openai', 'text-davinci-003', 'Hello from stdin', None)
    assert "response chunk" in result.output

def test_prompt_without_prompt(runner):
    result = runner.invoke(llx, ['prompt', '--target', 'ollama', '--model', 'llama3.2'])
    assert result.exit_code != 0
    assert "Prompt is required either as an argument or via stdin." in result.output


# LLX - A CLI for Interacting with Large Language Models

LLX is a Python-based command-line interface (CLI) that makes it easy to interact with various Large Language Model (LLM) providers. Whether you need to chat with models, send prompts with attachments, crawl URLs for content extraction, or run evaluations, LLX provides a convenient set of commands to streamline the process.

## Features

- Support for multiple LLM providers (OpenAI, Ollama, Anthropic, Deepseek, Mistral, Gemini, XAI).  
- LLM response streaming.  
- Multimodal support, upload and analyze files.  

## Installation

1. Make sure you have Python 3.7+ installed.  
2. (Optional) Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install LLX with pip:

   ```
   pip install llx
   ```

4. (Optional) Create a .env file in your project directory to store your provider API keys (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.). You can use .env.example as a reference.

## Usage

Once installed, you can run the CLI with:

```
llx --help
```

This will list all available subcommands and their required/optional parameters. Below is a summary of each subcommand and example usage.

----------------------------------------------------------------------
### 1. prompt
Send a single prompt to a specified model. The prompt text can be passed in directly or piped in via stdin.

• Required options:  
  --model / -m  : The model in "<provider>:<model_name>" format.  
• Optional:  
  --prompt / -p : The prompt string (if not provided, it reads from stdin).  
  --attachment / -a : Path to an image file to send as an attachment.

Example 1 (inline prompt):
```
llx prompt --model openai:gpt-3.5-turbo --prompt "Hello, how are you?"
```

Example 2 (pipe prompt from stdin):
```
echo "Hello from stdin" | llx prompt -m openai:gpt-3.5-turbo
```

Example 3 (with attachment):
```
llx prompt -m openai:gpt-3.5-turbo -p "Extract text from this image" -a /path/to/image.jpg
```

----------------------------------------------------------------------
### 2. chat
Start an interactive chat session with a specified model. Your local terminal will prompt for user input, and the assistant response will stream back.

• Required option:  
  --model / -m : The model in "<provider>:<model_name>" format.

Example:
```
llx chat --model openai:gpt-3.5-turbo
```
Then type your messages. Type /bye or press Ctrl+C to exit.

----------------------------------------------------------------------
### 3. server
Start a small FastAPI server to expose a chat completions endpoint (POST /v1/chat/completions). This is helpful if you want to run your own local API wrapper.

• Options:  
  --host : Defaults to 127.0.0.1.  
  --port : Defaults to 8000.

Example:
```
llx server --host 127.0.0.1 --port 8000
```
You can then send POST requests to http://127.0.0.1:8000/v1/chat/completions.

----------------------------------------------------------------------
### 4. url_to_prompt
Crawl one or more URLs, optionally extracting text from HTML, and print the content (plus an optional prompt) to stdout.

• Required option:  
  --url : The starting URL to begin crawling.  
• Optional:  
  --prompt / -p         : A prompt to prepend.  
  --extract-text        : Extract text instead of returning raw HTML.  
  --domain              : Restrict crawling to this domain.  
  --max-depth           : Depth of links to follow (defaults to 1).  
  --max-urls            : Max number of links to crawl (defaults to 1).

Example:
```
llx url_to_prompt --url https://example.com --prompt "Summarize the following:" --extract-text true --max-depth 2 --max-urls 5
```
This will print the extracted text from up to 5 URLs (within 2 link levels from the start) in a structured format alongside your prompt.

----------------------------------------------------------------------
### 5. files_to_prompt
Concatenate the contents of all files in a directory into a single prompt (printed to stdout). You can prepend an optional prompt string.

• Required options:  
  --path : Directory path containing the files.  
• Optional:  
  --prompt / -p : A prompt to prepend.

Example:
```
llx files_to_prompt --path /path/to/documents --prompt "Here are the contents of my documents:"
```
This command walks through each file, ignoring binary files, and combines them in an XML-like structure printed to stdout.

----------------------------------------------------------------------

## Environment Variables

Providers require API keys to function. Store them in a .env file in your working directory or set them directly in your shell environment. For example:

• OPENAI_API_KEY  
• ANTHROPIC_API_KEY  
• DEEPSEEK_API_KEY  
• MISTRAL_API_KEY  
• GEMINI_API_KEY  
• XAI_API_KEY
• PERPLEXITY_API_KEY

Use the .env.example file as a reference.

Example .env:
```
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>
...
```

----------------------------------------------------------------------

## Contributing

1. Clone the repository.  
2. Create and activate a virtual environment.  
3. Install dependencies by running pip install -e .  
4. Develop and submit pull requests.  

We appreciate bug reports, feature requests, and pull requests!

----------------------------------------------------------------------

## License

This project is licensed under the MIT License. See the LICENSE file for details.

----------------------------------------------------------------------

Happy prompting! If you have any questions or issues, feel free to open a GitHub issue.% 
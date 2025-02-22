# Perplexity Chat MCP Server

The Perplexity MCP Server provides a Python-based interface to the Perplexity API, offering tools for querying responses, maintaining chat history, and managing conversations. It supports model configuration via environment variables and stores chat data locally. Built with Hatch, it's designed for integration with development environments.

The MCP Server is desined to mimick how users interact with the Perplexity Chat on their browser by allowing your models to ask questions, continue conversations, and list all your chats.

[![smithery badge](https://smithery.ai/badge/@daniel-lxs/mcp-perplexity)](https://smithery.ai/server/@daniel-lxs/mcp-perplexity) [![Release and Publish](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/release.yml/badge.svg)](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/release.yml)



<a href="https://glama.ai/mcp/servers/0nggjl0ohi">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/0nggjl0ohi/badge" />
</a>

## Components

### Tools

- **ask_perplexity**: Request expert programming assistance through Perplexity. Focuses on coding solutions, error debugging, and technical explanations. Returns responses with source citations and alternative suggestions.
- **chat_perplexity**: Maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.
- **list_chats_perplexity**: Lists all available chat conversations with Perplexity AI. Returns chat IDs, titles, and creation dates (displayed in relative time format, e.g., "5 minutes ago", "2 days ago"). Results are paginated with 50 chats per page.
- **read_chat_perplexity**: Retrieves the complete conversation history for a specific chat. Returns the full chat history with all messages and their timestamps. No API calls are made to Perplexity - this only reads from local storage.

## Key Features

- **Model Configuration via Environment Variable:**  Allows you to specify the Perplexity model using the `PERPLEXITY_MODEL` environment variable for flexible model selection.

  You can also specify `PERPLEXITY_MODEL_ASK` and `PERPLEXITY_MODEL_CHAT` to use different models for the `ask_perplexity` and `chat_perplexity` tools, respectively.

  These will override `PERPLEXITY_MODEL`. You can check which models are available on the [Perplexity](https://docs.perplexity.ai/guides/model-cards) documentation.
- **Persistent Chat History:** The `chat_perplexity` tool maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.
- **Streaming Responses with Progress Reporting:** Uses progress reporting to prevent timeouts on slow responses.

## Quickstart

### Prerequisites

Before using this MCP server, ensure you have:

- Python 3.10 or higher
- [uvx](https://docs.astral.sh/uv/#installation) package manager installed

Note: Installation instructions for uvx are available [here](https://docs.astral.sh/uv/#installation).

### Configuration for All Clients

To use this MCP server, configure your client with these settings (configuration method varies by client):

```json
"mcpServers": {
  "mcp-perplexity": {
    "command": "uvx",
    "args": ["mcp-perplexity"],
    "env": {
      "PERPLEXITY_API_KEY": "your-api-key",
      "PERPLEXITY_MODEL": "sonar-pro",
      "DB_PATH": "chats.db"
    }
  }
}
```

**Key Configuration Notes:**
- Replace `"your-api-key"` with your Perplexity API key
- Environment variables can specify different models for ask/chat tools
- `DB_PATH` sets custom chat history location (default: chats.db)

### Cursor IDE Installation Helpers

For Cursor users, we provide automated scripts that:

1. Install uvx (Python package manager) if missing
2. Set up the `mcp-starter` helper tool
3. Generate appropriate Cursor command to be added to the MCP settings.

<details>
<summary><h5>Windows Installation</h5></summary>

1. Download the `install.ps1` script
2. Open PowerShell as Administrator
3. Allow script execution and run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\install.ps1
```

The script will:
- Check for required dependencies (curl, PowerShell)
- Install uvx if not present
- Install mcp-starter to `%USERPROFILE%\.local\bin`
- Create a configuration file at `%USERPROFILE%\.config\mcp-starter\config.json`
- Prompt for your Perplexity API key and model preferences
</details>

<details>
<summary><h5>Unix Installation (Linux/MacOS)</h5></summary>

1. Download the `install.sh` script
2. Open Terminal
3. Navigate to the directory containing the script
4. Make the script executable and run it:
```bash
chmod +x install.sh  # Only needed if downloaded directly from browser
./install.sh
```

The script will:
- Check for required dependencies (curl)
- Install uvx if not present
- Install mcp-starter to `$HOME/.local/bin`
- Create a configuration file at `$HOME/.config/mcp-starter/config.json`
- Prompt for your Perplexity API key and model preferences
</details>

#### Using Smithery CLI (Cursor Only)
```bash
npx -y @smithery/cli@latest run @daniel-lxs/mcp-perplexity --config "{\"perplexityApiKey\":\"pplx-abc\",\"perplexityModel\":\"sonar-pro\"}"
```

## Usage

### ask_perplexity

The `ask_perplexity` tool is used for specific questions, this tool doesn't maintain a chat history, every request is a new chat.

The tool will return a response from Perplexity AI using the `PERPLEXITY_MODEL_ASK` model if specified, otherwise it will use the `PERPLEXITY_MODEL` model.

### chat_perplexity

The `chat_perplexity` tool is used for ongoing conversations, this tool maintains a chat history.
A chat is identified by a chat ID, this ID is returned by the tool when a new chat is created. Chat IDs look like this: `wild-horse-12`.

This tool is useful for debugging, research, and any other task that requires a chat history.

The tool will return a response from Perplexity AI using the `PERPLEXITY_MODEL_CHAT` model if specified, otherwise it will use the `PERPLEXITY_MODEL` model.

### list_chats_perplexity
Lists all available chat conversations.  It returns a paginated list of chats, showing the chat ID, title, and creation time (in relative format).  You can specify the page number using the `page` argument (defaults to 1, with 50 chats per page).

### read_chat_perplexity
Retrieves the complete conversation history for a given `chat_id`.  This tool returns all messages in the chat, including timestamps and roles (user or assistant). This tool does *not* make any API calls to Perplexity; it only reads from the local database.


## Development

This project uses [Hatch](https://hatch.pypa.io/latest/) for development and builds. To get started:

1. Install Hatch (if not already installed):
   ```bash
   pip install hatch
   ```

2. Create and activate the Hatch environment:
   ```bash
   hatch env create
   hatch shell
   ```

3. Build the project:
   ```bash
   hatch build
   ```

The Hatch environment will automatically install all required dependencies.

## Contributing

This project is open to contributions. Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.





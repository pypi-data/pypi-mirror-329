# 🐰 Membit MCP Server

[![GitHub Repo Stars](https://img.shields.io/github/stars/bandprotocol/membit-mcp?style=social)](https://github.com/bandprotocol/membit-mcp) [![PyPI Downloads](https://img.shields.io/pypi/dm/membit-mcp)](https://pypi.org/project/membit-mcp/)

Membit MCP Server connects your AI systems to live social insights through Membit's API. By leveraging the Model Context Protocol (MCP), this server makes real-time social data—from trending discussion clusters to raw posts—readily available to your AI applications. Whether you're using Claude Desktop, Goose, Cursor, or any MCP-compatible client, this server enriches your model’s context with current social data.

---

## Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
  - [PyPI Package](#pypi-package)
  - [Clone from Git](#clone-from-git)
- [Client Configuration](#client-configuration)
  - [Using Cursor](#using-cursor)
  - [Using Claude Desktop](#using-claude-desktop)
- [How It Works](#how-it-works)
- [Example Interactions](#example-interactions)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [Credits](#credits)
- [License](#license)

---

## Introduction

Membit MCP Server is designed to empower AI agents with timely social context. It translates Membit's REST endpoints into MCP tools, allowing your AI to:

- **🔍 Discover Trending Discussions:** Search for and retrieve clusters of social discussions.
- **🕳️ Dive Deeper:** Fetch detailed posts and metadata for specific clusters.
- **🧠 Extract Insights:** Look up raw posts related to any keyword.

By integrating these capabilities, your AI can better understand and respond to rapidly evolving social narratives.

---

## Key Features

- **⚡️ Real-Time Data:** Pull live data from Membit's continuously updated API.
- **🔌 MCP Compatibility:** Seamlessly integrates with any client that supports the Model Context Protocol.
- **🚀 Simplicity & Flexibility:** A lightweight Python server that uses FastMCP for rapid development.

---

## Requirements

Make sure your system includes:

- A valid [Membit API key](https://membit.ai) (get one by registering on Membit)
- Python 3.10 or later (check with `python --version`)
- An MCP-capable client (e.g., [Claude Desktop](https://claude.ai/download) or [Goose](https://block.github.io/goose/))
- Git (if you plan to clone the repository)

---

## Use Without Installation

Make sure you have uv [installed](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer):

```bash
uvx membit-mcp
```

---

## Installation Guide

### PyPI Package

```bash
pip install membit-mcp
```

### Clone from Git

Alternatively, to work from the source:

1. Clone the repository:
   ```bash
   git clone https://github.com/membit-ai/membit-mcp.git
   cd membit-mcp
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the server:
   ```bash
   python membit_mcp.py
   ```

---

## Client Configuration

### Using Claude Desktop

For Claude Desktop, create or modify the configuration file:

- **macOS:** `$HOME/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Insert the following JSON snippet (substitute your API key):

```json
{
  "mcpServers": {
    "membit-mcp": {
      "command": "uvx",
      "args": ["membit-mcp"],
      "env": {
        "MEMBIT_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Using Goose

Goose is a lightweight MCP client that can integrate directly with your MCP servers. To use Membit MCP with Goose:

1. **Install Goose:** Follow the installation instructions on the [Goose website](https://block.github.io/goose/).
2. **Add Membit MCP Server in Goose:**
   - Open Goose’s configuration interface (Tools and Settings on the bottom right).
   - Extension > Add
   - Add a new MCP server with the following detail:
   - ID: `Membit`
   - Name: `Membit`
   - Command: `uvx membit-mcp`
   - Description: `Context-rich social insights and real-time discussions powered by Membit`
   - Environment Variables: `MEMBIT_API_KEY=your-api-key` (Don't for get to press `Add` button)
   - Ensure that the server is successfully added and that the tool list refreshes.
3. **Using the Tools:**  
   Once configured, Goose will display the tools:
   - **membit-clusters-search**
   - **membit-clusters-info**
   - **membit-posts-search**  
     You can now incorporate these tools into your agent workflows within Goose to fetch live social data.

### Using Cursor

1. Open Cursor’s settings.
2. Navigate to **Features > MCP Servers**.
3. Click **"+ Add New MCP Server"**.
4. Enter:
   - **Name:** `membit-mcp`
   - **Type:** `command`
   - **Command:**
     ```bash
     env MEMBIT_API_KEY=your-api-key uvx membit-mcp
     ```
     Replace `your-api-key` with your actual Membit API key.

---

## How It Works

The server uses the Model Context Protocol to expose three primary tools:

- **membit-clusters-search:**  
  Sends a GET request to `https://api.membit.com/clusters/search` with a query string and limit.
- **membit-clusters-info:**  
  Fetches details from `https://api.membit.com/clusters/info` using a cluster label.
- **membit-posts-search:**  
  Searches for raw social posts by keyword via `https://api.membit.com/posts/search`.

Each tool is accessible via MCP, and responses are formatted as human-readable JSON for easy integration.

---

## Example Interactions

- **Find Trending Topics:**  
  _Query:_ “membit-clusters-search for ‘cryptocurrency’”  
  _Response:_ A list of trending clusters discussing cryptocurrency.

- **Get Cluster Details:**  
  _Query:_ “membit-clusters-info for cluster labeled ‘crypto-trends’”  
  _Response:_ Detailed posts and metadata for that cluster.

- **Search for Specific Posts:**  
  _Query:_ “membit-posts-search for posts with ‘blockchain’”  
  _Response:_ Raw social post data containing the keyword “blockchain.”

These interactions allow your AI agent to draw on live social data in real time.

---

## FAQ & Troubleshooting

**Q:** _The server doesn’t start. What should I do?_  
**A:** Ensure you have Python 3.10+ installed and that the `MEMBIT_API_KEY` is correctly set in your environment.

**Q:** _I don’t see the tools in my MCP client._  
**A:** Try refreshing the server list. Also, check your server logs for any initialization errors.

**Q:** _I’m receiving API errors from Membit._  
**A:** Verify your Membit API key and confirm that your API usage hasn’t exceeded any limits.

---

## Credits

- **Membit:** For their robust social data API.
- **Model Context Protocol:** For the standardized framework that makes seamless integration possible.
- Special thanks to the open-source community for their continuous improvements.

---

## Development Guide

Make sure you have uv [installed](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer):

```bash
uv run poetry install
```

To run development server, use the following command:

```bash
uv run mcp dev membit_mcp.py
```

---

## License

This project is distributed under the MIT License.

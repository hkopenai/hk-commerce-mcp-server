# Hong Kong Commerce MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-commerce-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to commerce-related data through a FastMCP interface.

## Features

### Hotel Room Occupancy Rate
- Get hotel room occupancy rate data in Hong Kong

## Data Source

- Culture, Sports and Tourism Bureau

## Examples

* Get hotel room occupancy rate data in Hong Kong

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### Running Options

- Default stdio mode: `python server.py`
- SSE mode (port 8000): `python server.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-commerce": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hkopenai.hk-commerce-mcp-server"
    ]
  }
}
```

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```

"""
Main entry point for the HK OpenAI Commerce MCP Server.

This module handles command-line arguments and initiates the main server functionality.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(main, "HK Commerce MCP Server")

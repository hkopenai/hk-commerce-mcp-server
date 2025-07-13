"""
Module for creating and running the HK OpenAI Commerce MCP Server.

This module provides functionality to initialize and run a server for handling
commerce-related data queries in Hong Kong, using the FastMCP framework.
"""

import argparse

from fastmcp import FastMCP

from hkopenai.hk_commerce_mcp_server import tool_hotel_room_occupancy_rate


def create_mcp_server():
    """
    Create and configure the MCP server.
    
    Returns:
        FastMCP: Configured MCP server instance ready to handle data queries.
    """
    mcp = FastMCP(name="HK OpenAI commerce Server")

    tool_hotel_room_occupancy_rate.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the MCP Server.
    
    Parses command line arguments to determine the mode of operation (SSE or stdio)
    and starts the server accordingly.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"MCP Server running in SSE mode on port {port}, bound to {host}")
    else:
        server.run()
        print("MCP Server running in stdio mode")


if __name__ == "__main__":
    main()

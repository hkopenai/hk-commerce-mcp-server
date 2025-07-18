"""
Module for creating and running the HK OpenAI Commerce MCP Server.

This module provides functionality to initialize and run a server for handling
commerce-related data queries in Hong Kong, using the FastMCP framework.
"""

import argparse

from fastmcp import FastMCP

from .tools import hotel_room_occupancy_rate


def server():
    """
    Create and configure the MCP server.

    Returns:
        FastMCP: Configured MCP server instance ready to handle data queries.
    """
    mcp = FastMCP(name="HK OpenAI commerce Server")

    hotel_room_occupancy_rate.register(mcp)

    return mcp

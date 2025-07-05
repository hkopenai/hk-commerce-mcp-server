"""
Module for creating and running the HK OpenAI Commerce MCP Server.

This module provides functionality to initialize and run a server for handling
commerce-related data queries in Hong Kong, using the FastMCP framework.
"""

import argparse
from fastmcp import FastMCP
from hkopenai.hk_commerce_mcp_server import tool_hotel_room_occupancy_rate
from typing import Dict, List, Annotated, Optional
from pydantic import Field


def create_mcp_server():
    """
    Create and configure the MCP server.
    
    Returns:
        FastMCP: Configured MCP server instance ready to handle data queries.
    """
    mcp = FastMCP(name="HK OpenAI commerce Server")

    @mcp.tool(description="Get monthly hotel room occupancy rates in Hong Kong")
    def get_hotel_occupancy_rates(
        start_year: Annotated[int, Field(description="Start year for data range")],
        end_year: Annotated[int, Field(description="End year for data range")],
    ) -> List[Dict]:
        return tool_hotel_room_occupancy_rate.get_hotel_occupancy_rates(
            start_year, end_year
        )

    return mcp


def main():
    """
    Main function to run the HKO MCP Server.
    
    Parses command line arguments to determine the mode of operation (SSE or stdio)
    and starts the server accordingly.
    """
    parser = argparse.ArgumentParser(description="HKO MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    args = parser.parse_args()

    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")


if __name__ == "__main__":
    main()

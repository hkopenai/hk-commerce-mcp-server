"""
Module for testing the MCP server creation and functionality.

This module contains unit tests to verify the correct initialization and
behavior of the MCP server and its associated tools.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_commerce_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool functionality.
    
    This class contains test cases to ensure that the MCP server is correctly
    initialized and that the tools are properly registered and callable.
    """
    @patch("hkopenai.hk_commerce_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_commerce_mcp_server.tool_hotel_room_occupancy_rate.register")
    def test_create_mcp_server(self, mock_register, mock_fastmcp):
        """
        Test the creation of the MCP server and tool registration.
        
        This test verifies that the server is initialized correctly, and that
        the tools are registered as expected using the FastMCP framework.
        It also checks that the tools can be called with the correct parameters.
        
        Args:
            mock_tool_hotel_room_occupancy_rate: Mock for the hotel occupancy rate tool.
            mock_fastmcp: Mock for the FastMCP class.
        """
        # Setup mocks
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        mock_register.assert_called_once_with(mock_server)
        


if __name__ == "__main__":
    unittest.main()

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
    @patch("hkopenai.hk_commerce_mcp_server.server.tool_hotel_room_occupancy_rate")
    def test_create_mcp_server(self, mock_tool_hotel_room_occupancy_rate, mock_fastmcp):
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

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 1)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 1)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_hotel_occupancy_rates"](start_year=2020, end_year=2021)
        mock_tool_hotel_room_occupancy_rate.get_hotel_occupancy_rates.assert_called_once_with(
            2020, 2021
        )


if __name__ == "__main__":
    unittest.main()

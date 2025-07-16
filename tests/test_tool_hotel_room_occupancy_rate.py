"""
Module for testing the hotel room occupancy rate tool.

This module contains unit tests for fetching and filtering hotel room occupancy rate data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_commerce_mcp_server.tools.hotel_room_occupancy_rate import (
    _get_hotel_occupancy_rates,
)
from hkopenai.hk_commerce_mcp_server.tools.hotel_room_occupancy_rate import register


class TestHotelRoomOccupancyRate(unittest.TestCase):
    """
    Test class for verifying hotel room occupancy rate functionality.

    This class contains test cases to ensure the data fetching and filtering
    for hotel room occupancy rates work as expected.
    """

    def test_get_hotel_occupancy_rates(self):
        """
        Test the retrieval and filtering of hotel room occupancy rates.

        This test verifies that the function correctly filters data by year range,
        returns empty results for non-matching years, and handles partial year matches.
        """

        with patch(
            "hkopenai.hk_commerce_mcp_server.tools.hotel_room_occupancy_rate.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            mock_fetch_csv_from_url.return_value = [
                {"Year-Month": "2019-01", "Hotel_room_occupancy_rate(%)": "91.0"},
                {"Year-Month": "2019-02", "Hotel_room_occupancy_rate(%)": "92.0"},
                {"Year-Month": "2020-01", "Hotel_room_occupancy_rate(%)": "80.0"},
            ]

            # Test filtering by year range
            result = _get_hotel_occupancy_rates(2019, 2019)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["year_month"], "2019-01")
            self.assertEqual(result[1]["year_month"], "2019-02")

            # Test empty result for non-matching years
            result = _get_hotel_occupancy_rates(2021, 2022)
            self.assertEqual(len(result), 0)

            # Test partial year match
            result = _get_hotel_occupancy_rates(2019, 2020)
            self.assertEqual(len(result), 3)

    def test_register_tool(self):
        """
        Test the registration of the get_hotel_occupancy_rates tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_hotel_occupancy_rates function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get monthly hotel room occupancy rates in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_hotel_occupancy_rates")

        # Call the decorated function and verify it calls _get_hotel_occupancy_rates
        with patch(
            "hkopenai.hk_commerce_mcp_server.tools.hotel_room_occupancy_rate._get_hotel_occupancy_rates"
        ) as mock_get_hotel_occupancy_rates:
            decorated_function(start_year=2018, end_year=2019)
            mock_get_hotel_occupancy_rates.assert_called_once_with(2018, 2019)

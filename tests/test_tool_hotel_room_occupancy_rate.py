"""
Module for testing hotel room occupancy rate tool functionality.

This module contains unit tests to verify the correct fetching and processing
of hotel room occupancy data for Hong Kong.
"""

import unittest
from unittest.mock import patch
from hkopenai.hk_commerce_mcp_server.tool_hotel_room_occupancy_rate import (
    fetch_hotel_occupancy_data,
    get_hotel_occupancy_rates,
)


class TestHotelRoomOccupancy(unittest.TestCase):
    """
    Test class for verifying hotel room occupancy rate tool functionality.
    
    This class contains test cases to ensure that the data fetching and processing
    functions for hotel room occupancy rates work as expected with mocked data.
    """
    CSV_DATA = """Year-Month,Hotel_room_occupancy_rate(%)
202004,34
202005,37
202006,44
202007,49
202008,50
202009,52
202010,55
202104,40
202105,45
202106,60
202107,65
202108,70
202109,75"""

    def setUp(self):
        self.mock_requests = patch("requests.get").start()
        mock_response = self.mock_requests.return_value
        mock_response.text = self.CSV_DATA
        self.addCleanup(patch.stopall)

    def test_fetch_hotel_occupancy_data(self):
        """
        Test fetching hotel room occupancy data.
        
        This test verifies that the function fetches data correctly using a mocked
        HTTP response and checks the structure and content of the returned data.
        """
        result = fetch_hotel_occupancy_data()
        self.assertEqual(len(result), 13)
        self.assertEqual(result[0]["Year-Month"], "202004")
        self.assertEqual(result[0]["Hotel_room_occupancy_rate(%)"], "34")
        self.assertEqual(result[-1]["Year-Month"], "202109")
        self.assertEqual(result[-1]["Hotel_room_occupancy_rate(%)"], "75")

    def test_get_hotel_occupancy_rates(self):
        """
        Test processing hotel room occupancy rates for specific year ranges.
        
        This test verifies that the function correctly filters and returns data
        for the specified year ranges, including full range, single year 2020,
        and single year 2021.
        """
        # Test full range
        result = get_hotel_occupancy_rates(2020, 2021)
        self.assertEqual(len(result), 13)

        # Test 2020 only
        result = get_hotel_occupancy_rates(2020, 2020)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]["year_month"], "202004")
        self.assertEqual(result[-1]["year_month"], "202010")

        # Test 2021 only
        result = get_hotel_occupancy_rates(2021, 2021)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0]["year_month"], "202104")
        self.assertEqual(result[-1]["year_month"], "202109")


if __name__ == "__main__":
    unittest.main()

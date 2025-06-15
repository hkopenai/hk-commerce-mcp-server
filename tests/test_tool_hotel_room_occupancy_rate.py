import unittest
from unittest.mock import patch
from hkopenai.hk_commerce_mcp_server.tool_hotel_room_occupancy_rate import (
    fetch_hotel_occupancy_data,
    get_hotel_occupancy_rates
)

class TestHotelRoomOccupancy(unittest.TestCase):
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
        self.mock_requests = patch('requests.get').start()
        mock_response = self.mock_requests.return_value
        mock_response.text = self.CSV_DATA
        self.addCleanup(patch.stopall)

    def test_fetch_hotel_occupancy_data(self):
        result = fetch_hotel_occupancy_data()
        self.assertEqual(len(result), 13)
        self.assertEqual(result[0]['Year-Month'], '202004')
        self.assertEqual(result[0]['Hotel_room_occupancy_rate(%)'], '34')
        self.assertEqual(result[-1]['Year-Month'], '202109')
        self.assertEqual(result[-1]['Hotel_room_occupancy_rate(%)'], '75')

    def test_get_hotel_occupancy_rates(self):
        # Test full range
        result = get_hotel_occupancy_rates(2020, 2021)
        self.assertEqual(len(result), 13)
        
        # Test 2020 only
        result = get_hotel_occupancy_rates(2020, 2020)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0]['year_month'], '202004')
        self.assertEqual(result[-1]['year_month'], '202010')
        
        # Test 2021 only
        result = get_hotel_occupancy_rates(2021, 2021)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0]['year_month'], '202104')
        self.assertEqual(result[-1]['year_month'], '202109')

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_commerce_mcp_server.app import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_commerce_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_commerce_mcp_server.app.tool_hotel_room_occupancy_rate')
    def test_create_mcp_server(self, mock_tool_hotel, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
        # Track decorator calls and capture decorated function
        decorator_calls = []
        decorated_func = None
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                nonlocal decorated_func
                decorated_func = f
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_fastmcp.return_value = mock_server
        mock_tool_hotel.get_hotel_occupancy_rates.return_value = [{'year_month': '2020-01', 'occupancy_rate': 85.5}]

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tool was decorated
        self.assertIsNotNone(decorated_func)
        
        # Test the actual decorated function
        result = decorated_func(2020, 2020)
        mock_tool_hotel.get_hotel_occupancy_rates.assert_called_once_with(2020, 2020)

if __name__ == "__main__":
    unittest.main()

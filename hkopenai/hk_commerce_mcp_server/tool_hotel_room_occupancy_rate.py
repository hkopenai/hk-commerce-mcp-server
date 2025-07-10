"""
Module for fetching and processing hotel room occupancy rate data in Hong Kong.

This module provides functions to retrieve hotel occupancy data from an external
source and filter it based on specified year ranges for use in the MCP server.
"""

import requests
from typing import List, Dict
from pydantic import Field
from typing_extensions import Annotated
import csv
from io import StringIO


def fetch_hotel_occupancy_data() -> List[Dict]:
    """Fetch hotel occupancy data from Culture, Sports and Tourism Bureau"""
    url = "https://www.tourism.gov.hk/datagovhk/hotelroomoccupancy/hotel_room_occupancy_rate_monthly_en.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        return list(reader)
    except requests.exceptions.RequestException as e:
        # Handle network errors or invalid HTTP responses
        return {"error": f"Failed to fetch data from {url}: {e}"}
    except Exception as e:
        # Handle other potential errors during CSV processing
        return {"error": f"An unexpected error occurred during data processing: {e}"}


def get_hotel_occupancy_rates(
    start_year: Annotated[int, Field(description="Start year for data range")],
    end_year: Annotated[int, Field(description="End year for data range")],
) -> List[Dict]:
    """Get monthly hotel room occupancy rates in Hong Kong

    Args:
        start_year: First year to include in results
        end_year: Last year to include in results

    Returns:
        List of monthly occupancy rates with year-month and percentage
    """
    data = fetch_hotel_occupancy_data()
    filtered_data = []
    for row in data:
        year = int(row["Year-Month"][:4])
        if start_year <= year <= end_year:
            filtered_data.append(
                {
                    "year_month": row["Year-Month"],
                    "occupancy_rate": float(row["Hotel_room_occupancy_rate(%)"]),
                }
            )
    return filtered_data

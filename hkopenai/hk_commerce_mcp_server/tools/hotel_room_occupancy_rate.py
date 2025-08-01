"""
Module for fetching and processing hotel room occupancy rate data in Hong Kong.

This module provides functions to retrieve hotel occupancy data from an external
source and filter it based on specified year ranges for use in the MCP server.
"""

import csv
import io
from typing import Dict, List
from hkopenai_common.csv_utils import fetch_csv_from_url
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the hotel room occupancy rate tool with the FastMCP server."""

    @mcp.tool(description="Get monthly hotel room occupancy rates in Hong Kong")
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
        return _get_hotel_occupancy_rates(start_year, end_year)


def _get_hotel_occupancy_rates(
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
    url = "https://www.tourism.gov.hk/datagovhk/hotelroomoccupancy/hotel_room_occupancy_rate_monthly_en.csv"
    data = fetch_csv_from_url(url)

    if "error" in data:
        return data

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

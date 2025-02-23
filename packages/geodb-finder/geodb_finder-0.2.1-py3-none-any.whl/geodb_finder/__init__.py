# flake8: noqa: E501
# We're using type hints and sometimes they make lines longer than 79 chars.
# Rather than making the code less readable by breaking everything into multiple
# lines, we'll disable the line length check for this file.

import os
import logging
import asyncio
import aiosqlite
from typing import Optional, Dict, List, Any


class GeoDBFinder:
    """Handles database interactions for geolocation data."""

    def __init__(self):
        self.db_path = os.path.join(
            os.path.dirname(__file__), "data", "geolocations.db"
        )

    async def _fetch_one(
        self, query: str, params: tuple
    ) -> Optional[Dict[str, str]]:
        """Executes a query and returns a single result as a dictionary."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params)
            result = await cursor.fetchone()
            return dict(result) if result else None

    async def _fetch_all(
        self, query: str, params: tuple
    ) -> List[Dict[str, str]]:
        """Executes a query and returns all results as a list."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params)
            results = await cursor.fetchall()
            return [dict(row) for row in results]

    async def search_location_async(
        self, city_name: str, country: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously searches for a location in the database.

        Args:
            city_name (str): Name of the city to search for.
            country (Optional[str]): Country name to filter results.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing location data.
        """
        query = """
            SELECT city_name, longitude, latitude, timezone, country
            FROM records
            WHERE LOWER(city_name) = LOWER(?)
        """
        params = (city_name,)

        if country:
            query += " AND LOWER(country) = LOWER(?)"
            params += (country,)

        query += " LIMIT 1"
        results = await self._fetch_all(query, params)
        logging.debug(f"Query result for {city_name}, {country}: {results}")
        for result in results:
            result["city"] = result.pop("city_name")
        return results

    def search_location(
        self, city_name: str, country: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Synchronously searches for a location in the database.

        Args:
            city_name (str): Name of the city to search for.
            country (Optional[str]): Country name to filter results.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing location data.
        """
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(
                self.search_location_async(city_name, country)
            )
        finally:
            loop.close()

    async def search_by_coordinates_async(
        self, latitude: str, longitude: str, limit: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously searches for a location in the database using coordinates.

        Args:
            latitude (str): Latitude coordinate.
            longitude (str): Longitude coordinate.
            limit (int): Maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing location data.
        """
        query = """
            SELECT city_name, longitude, latitude, timezone, country
            FROM records
            WHERE latitude = ? AND longitude = ?
            LIMIT ?
        """
        params = (latitude, longitude, limit)
        results = await self._fetch_all(query, params)
        
        for result in results:
            result["city"] = result.pop("city_name")
        return results

    def search_by_coordinates(
        self, latitude: str, longitude: str, limit: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Synchronously searches for a location in the database using coordinates.

        Args:
            latitude (str): Latitude coordinate.
            longitude (str): Longitude coordinate.
            limit (int): Maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing location data.
        """
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(
                self.search_by_coordinates_async(latitude, longitude, limit)
            )
        finally:
            loop.close()

    async def list_countries_async(self) -> List[Dict[str, str]]:
        """
        Asynchronously fetches a list of distinct country names.

        Returns:
            List[Dict[str, str]]: A list of country dictionaries.
        """
        query = "SELECT DISTINCT country FROM records ORDER BY country"
        return await self._fetch_all(query, ())

    def list_countries(self) -> List[Dict[str, str]]:
        """
        Synchronously fetches a list of distinct country names.

        Returns:
            List[Dict[str, str]]: A list of country dictionaries.
        """
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.list_countries_async())
        finally:
            loop.close()


# Singleton instance
_finder = GeoDBFinder()


def search_location(
    city_name: str, country: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for a location by city name and optionally country."""
    return _finder.search_location(city_name, country)


async def search_location_async(
    city_name: str, country: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Asynchronously search for a location by city name and optionally country."""
    return await _finder.search_location_async(city_name, country)


def search_by_coordinates(
    latitude: str, longitude: str, limit: int = 1
) -> List[Dict[str, Any]]:
    """Search for a location by latitude and longitude."""
    return _finder.search_by_coordinates(latitude, longitude, limit)


async def search_by_coordinates_async(
    latitude: str, longitude: str, limit: int = 1
) -> List[Dict[str, Any]]:
    """Asynchronously search for a location by latitude and longitude."""
    return await _finder.search_by_coordinates_async(latitude, longitude, limit)


def list_countries() -> List[Dict[str, str]]:
    """Fetch a list of distinct country names from the database."""
    return _finder.list_countries()


async def list_countries_async() -> List[Dict[str, str]]:
    """Asynchronously fetch a list of distinct country names."""
    return await _finder.list_countries_async()

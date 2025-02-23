import pytest
from geodb_finder import (
    search_location, search_location_async,
    search_by_coordinates, search_by_coordinates_async,
    list_countries, list_countries_async
)


def test_sync_search():
    # Test synchronous search
    result = search_location("Amsterdam")
    print("Sync search result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] in ["Amsterdam", "A'dam/dam"]
    assert result[0]["country"] == "Netherlands"
    assert "longitude" in result[0]
    assert "latitude" in result[0]
    assert "timezone" in result[0]

    # Test with country filter
    result = search_location("London", "United Kingdom")
    print("Sync search with country result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] == "London"
    assert result[0]["country"] == "United Kingdom"


def test_search_by_coordinates():
    # Test synchronous search by coordinates
    result = search_by_coordinates("52n22", "4e53")
    print("Sync search by coordinates result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] in ["Amsterdam", "A'dam/dam"]
    assert result[0]["country"] == "Netherlands"
    assert "longitude" in result[0]
    assert "latitude" in result[0]
    assert "timezone" in result[0]


def test_search_by_coordinates_multiple():
    # Test synchronous search with multiple results
    results = search_by_coordinates("52n22", "4e53", limit=3)
    print("Sync search by coordinates (multiple) result:", results)
    assert isinstance(results, list)
    assert len(results) > 1  # Ensure multiple results are returned


def test_list_countries_sync():
    # Test synchronous list_countries
    countries = list_countries()
    print("Sync list_countries result:", countries)
    assert isinstance(countries, list)
    assert len(countries) > 0
    country_names = [entry["country"] for entry in countries]
    assert "Netherlands" in country_names


@pytest.mark.asyncio
async def test_search_by_coordinates_multiple_async():
    # Test asynchronous search with multiple results
    results = await search_by_coordinates_async("52n22", "4e53", limit=3)
    print("Async search by coordinates (multiple) result:", results)
    assert isinstance(results, list)
    assert len(results) > 1  # Ensure multiple results are returned


@pytest.mark.asyncio
async def test_list_countries_async():
    # Test asynchronous list_countries_async
    countries = await list_countries_async()
    print("Async list_countries result:", countries)
    assert isinstance(countries, list)
    assert len(countries) > 0
    country_names = [entry["country"] for entry in countries]
    assert "Netherlands" in country_names

    # Test asynchronous search by coordinates
    result = await search_by_coordinates_async("52n22", "4e53")
    print("Async search by coordinates result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] in ["Amsterdam", "A'dam/dam"]
    assert result[0]["country"] == "Netherlands"
    assert "longitude" in result[0]
    assert "latitude" in result[0]
    assert "timezone" in result[0]

    result = await search_location_async("Amsterdam")
    print("Async search result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] == "Amsterdam"
    assert result[0]["country"] == "Netherlands"
    assert "longitude" in result[0]
    assert "latitude" in result[0]
    assert "timezone" in result[0]

    # Test with country filter
    result = await search_location_async("London", "United Kingdom")
    print("Async search with country result:", result)
    assert result is not None
    assert len(result) > 0
    assert result[0]["city"] == "London"
    assert result[0]["country"] == "United Kingdom"

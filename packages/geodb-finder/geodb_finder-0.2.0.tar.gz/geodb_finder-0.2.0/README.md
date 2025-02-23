# geodb-finder

`geodb-finder` is a Python package that allows you to retrieve geographical information such as latitude, longitude, timezone ID, and country using a city or location name. Additionally, it supports searching for the same information using latitude and longitude.

## Installation

Install the package using pip:

```bash
pip install geodb-finder
```

Requires Python 3.7 or higher for async/await support.

## Usage

### Find Location Information by City Name

You can retrieve latitude, longitude, timezone ID, and country by providing a city name.

```python
from geodb_finder import search_location

# Search for a city
results = search_location("London")
if results:
    city_info = results[0]  # Get the first match
    print(city_info)  # Dictionary with latitude, longitude, timezone, and country

# Search with country filter
results = search_location("London", country="United Kingdom")
if results:
    city_info = results[0]
    print(f"Found: {city_info['city']}, {city_info['country']}")
```

All functions return results as a list of dictionaries, where each dictionary contains:
- `city`: The city name
- `country`: The country name
- `latitude`: The latitude coordinate
- `longitude`: The longitude coordinate
- `timezone`: The timezone identifier

**Note:** An asynchronous version of this function is available as `search_location_async(city_name: str, country: Optional[str] = None)`.

### Find Location Information by Coordinates

You can retrieve location details using latitude and longitude coordinates. The function supports returning multiple results.

```python
from geodb_finder import search_by_coordinates

# Search by latitude and longitude with limit
results = search_by_coordinates("52n22", "4e53", limit=3)  # Returns up to 3 matches
for location in results:
    print(f"Found: {location['city']}, {location['country']}")
```

The `limit` parameter controls how many results to return (default is 1). This is useful when multiple cities share the same coordinates.

**Note:** An asynchronous version of this function is available as `search_by_coordinates_async(latitude: str, longitude: str, limit: int = 1)`.

**Important:** The database stores coordinates in a specific format:
- Latitude: Degrees followed by 'n' (north) or 's' (south), e.g., `"52n22"`, `"34s45"`
- Longitude: Degrees followed by 'e' (east) or 'w' (west), e.g., `"4e53"`, `"2w30"`

### List Available Countries

You can retrieve a list of all available countries in the database.

```python
from geodb_finder import list_countries

# Get all countries
countries = list_countries()
for country_info in countries:
    print(country_info['country'])  # Prints each country name
```

**Note:** An asynchronous version of this function is available as `list_countries_async()`.

### Async Usage Examples

For async applications, all functions have async counterparts:

```python
import asyncio
from geodb_finder import search_location_async, search_by_coordinates_async

async def main():
    # Search by city name
    results = await search_location_async("Amsterdam")
    if results:
        print(f"Found city: {results[0]['city']}")

    # Search by coordinates with multiple results
    locations = await search_by_coordinates_async("52n22", "4e53", limit=2)
    for loc in locations:
        print(f"Found location: {loc['city']}, {loc['country']}")

    # Search with country filter
    results = await search_location_async("London", country="United Kingdom")
    if results:
        print(f"Found city in UK: {results[0]['city']}")

# Run the async example
asyncio.run(main())
```

## Running Tests

To run the test suite, use:

```bash
pytest
```

Ensure you have `pytest` installed:

```bash
pip install pytest
```

## Development

When contributing, ensure you have development dependencies installed:

```bash
pip install -e ".[dev]"
```

The package uses:
- `pytest` for testing
- `flake8` for code style
- `black` for code formatting

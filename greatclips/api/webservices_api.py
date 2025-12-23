"""API client for webservices.greatclips.com endpoints."""

import json
import urllib.request
import urllib.error
from typing import Dict, Any


BASE_URL = "https://webservices.greatclips.com"


class WebservicesAPIError(Exception):
    """Custom exception for webservices API errors."""
    pass


def search_stores_by_term(
    term: str,
    radius: int = 50,
    limit: int = 50,
    lat: float = 0,
    lng: float = 0,
    access_token: str = ""
) -> Dict[str, Any]:
    """
    Search for stores by term (zip code, city name, etc).

    This endpoint requires a Great Clips access token obtained from the
    authentication/token endpoint.

    Args:
        term: Search term (zip code, city name, etc)
        radius: Search radius in miles (default: 50)
        limit: Maximum number of results (default: 50)
        lat: Latitude (default: 0)
        lng: Longitude (default: 0)
        access_token: Great Clips API access token (required)

    Returns:
        Dictionary containing matching stores

    Raises:
        WebservicesAPIError: If the API request fails
    """
    if not access_token:
        raise WebservicesAPIError("access_token is required for store search")

    url = f"{BASE_URL}/customer/salon-search/term"

    payload_json = json.dumps({
        "term": term,
        "radius": radius,
        "limit": str(limit),
        "lat": lat,
        "lng": lng
    })

    request = urllib.request.Request(
        url,
        data=payload_json.encode('utf-8'),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise WebservicesAPIError(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise WebservicesAPIError(f"Search request failed: {str(e)}")


def search_stores_by_point(
    latitude: float,
    longitude: float,
    radius: int = 50,
    limit: int = 50,
    access_token: str = ""
) -> Dict[str, Any]:
    """
    Search for stores near a specific coordinate (point).

    This endpoint requires a Great Clips access token obtained from the
    authentication/token endpoint.

    Args:
        latitude: Latitude of the center point
        longitude: Longitude of the center point
        radius: Search radius in miles (default: 50)
        limit: Maximum number of results (default: 50)
        access_token: Great Clips API access token (required)

    Returns:
        Dictionary containing nearby stores

    Raises:
        WebservicesAPIError: If the API request fails
    """
    if not access_token:
        raise WebservicesAPIError("access_token is required for store search")

    url = f"{BASE_URL}/customer/salon-search/point"

    payload_json = json.dumps({
        "lat": latitude,
        "lng": longitude,
        "radius": radius,
        "limit": str(limit)
    })

    request = urllib.request.Request(
        url,
        data=payload_json.encode('utf-8'),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise WebservicesAPIError(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise WebservicesAPIError(f"Search request failed: {str(e)}")


def search_stores_by_rect(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
    radius: int = 50,
    limit: int = 50,
    access_token: str = ""
) -> Dict[str, Any]:
    """
    Search for stores within a rectangular area (map bounds).

    This endpoint requires a Great Clips access token obtained from the
    authentication/token endpoint.

    Args:
        lat1: Latitude of first corner
        lng1: Longitude of first corner
        lat2: Latitude of second corner
        lng2: Longitude of second corner
        radius: Search radius in miles (default: 50)
        limit: Maximum number of results (default: 50)
        access_token: Great Clips API access token (required)

    Returns:
        Dictionary containing stores in the rectangle

    Raises:
        WebservicesAPIError: If the API request fails
    """
    if not access_token:
        raise WebservicesAPIError("access_token is required for store search")

    url = f"{BASE_URL}/customer/salon-search/rect"

    payload_json = json.dumps({
        "lat1": lat1,
        "lng1": lng1,
        "lat2": lat2,
        "lng2": lng2,
        "radius": radius,
        "limit": str(limit)
    })

    request = urllib.request.Request(
        url,
        data=payload_json.encode('utf-8'),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise WebservicesAPIError(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise WebservicesAPIError(f"Search request failed: {str(e)}")

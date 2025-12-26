"""API client for stylewaretouch.net endpoints."""

import json
import time
import urllib.error
import urllib.request
from typing import Any

from greatclips.api.auth.auth import get_encrypted_token

BASE_URL = "https://www.stylewaretouch.net/api"


class APIError(Exception):
    """Custom exception for API errors."""

    pass


def _make_request(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    """
    Make an authenticated request to stylewaretouch.net API.

    Args:
        endpoint: The API endpoint (e.g., "store/waitTime")
        payload: The request payload as a dictionary

    Returns:
        JSON response as a dictionary

    Raises:
        APIError: If the request fails
    """
    # Prepare payload
    payload_json = json.dumps(payload)
    timestamp_ms = str(int(time.time() * 1000))

    # Generate authentication token
    auth_token = get_encrypted_token(f"{timestamp_ms}{payload_json}")

    # Build URL
    url = f"{BASE_URL}/{endpoint}?t={timestamp_ms}&s={auth_token}"

    # Create request
    request = urllib.request.Request(
        url,
        data=payload_json.encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    # Make request
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise APIError(f"HTTP {e.code}: {error_body}")
    except Exception as e:
        raise APIError(f"Request failed: {str(e)}")


def get_wait_times(store_numbers: list[int]) -> dict[str, Any]:
    """
    Fetch wait times for one or more store numbers.

    Args:
        store_numbers: List of store numbers (e.g., [8874])

    Returns:
        Dictionary containing wait time data for each store

    Raises:
        APIError: If the API request fails
    """
    payload = [{"storeNumber": str(num)} for num in store_numbers]
    return _make_request("store/waitTime", payload)


def check_in_customer(
    store_number: int,
    name: str,
    phone: str,
    guests: int = 1,
    ip_address: str = "",
    profile_id: str = "",
    **kwargs,
) -> dict[str, Any]:
    """
    Check a customer in to a salon.

    Args:
        store_number: Store number
        name: Customer name
        phone: Customer phone number
        guests: Number of guests (default: 1)
        ip_address: Customer IP address
        profile_id: Customer profile ID

    Returns:
        Check-in confirmation data

    Raises:
        APIError: If the API request fails
    """
    payload = {
        "storeNumber": store_number,
        "name": name,
        "phone": phone,
        "guests": guests,
        "ipAddress": ip_address,
        "profileId": profile_id,
        "source": "Browser",
    }
    return _make_request("customer/checkIn", payload)


def cancel_check_in(
    oci_id: str,
    store_number: int,
    phone: str,
    guests: int = 1,
    ip_address: str = "",
    name: str = "",
    **kwargs,
) -> dict[str, Any]:
    """
    Cancel an existing check-in.

    Args:
        oci_id: OCI ID from the check-in
        store_number: Store number
        phone: Customer phone number
        guests: Number of guests (default: 1)
        ip_address: Customer IP address
        name: Customer name

    Returns:
        Cancellation confirmation data

    Raises:
        APIError: If the API request fails
    """
    payload = {
        "computerId": "",
        "phone": phone,
        "guests": guests,
        "ociId": oci_id,
        "ipAddress": ip_address,
        "name": name,
        "storeNumber": store_number,
        "source": "Browser",
    }
    return _make_request("customer/cancel", payload)


def get_customer_status(
    oci_id: str,
    store_number: int,
    phone: str,
    guests: int = 1,
    ip_address: str = "",
    profile_id: str = "",
    name: str = "",
    **kwargs,
) -> dict[str, Any]:
    """
    Get the current status of a customer's check-in.

    Args:
        oci_id: OCI ID from the check-in
        store_number: Store number
        phone: Customer phone number
        guests: Number of guests (default: 1)
        ip_address: Customer IP address
        profile_id: Customer profile ID
        name: Customer name

    Returns:
        Current check-in status and position in queue

    Raises:
        APIError: If the API request fails
    """
    payload = {
        "computerId": "",
        "phone": phone,
        "guests": guests,
        "ociId": oci_id,
        "source": "Browser",
        "ipAddress": ip_address,
        "profileId": profile_id,
        "name": name,
        "storeNumber": store_number,
    }
    return _make_request("customer/status", payload)

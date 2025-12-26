"""Token management for webservices.greatclips.com API."""

import json
import urllib.error
import urllib.request

BASE_URL = "https://webservices.greatclips.com"
TOKEN_ENDPOINT = f"{BASE_URL}/customer/authentication/token"


class TokenManagerError(Exception):
    """Custom exception for token generation errors."""

    pass


class TokenManager:
    """Manages authentication tokens for webservices.greatclips.com."""

    def __init__(self, endpoint: str = TOKEN_ENDPOINT):
        """
        Initialize token manager.

        Args:
            endpoint: The authentication token endpoint URL
        """
        self.endpoint = endpoint

    def fetch_token(self) -> str:
        """
        Fetch a new authentication token from the Great Clips API.

        Makes a request to the /customer/authentication/token endpoint to obtain
        an access token for use with other webservices.greatclips.com endpoints.

        Returns:
            The access token string

        Raises:
            TokenManagerError: If token fetch fails

        Example:
            >>> manager = TokenManager()
            >>> token = manager.fetch_token()
        """
        try:
            # Create HTTP request
            request = urllib.request.Request(
                self.endpoint,
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
            )

            # Execute request
            with urllib.request.urlopen(request) as response:
                # Check response status
                if response.status != 200:
                    raise TokenManagerError(
                        f"Invalid response status: {response.status}"
                    )

                # Parse JSON response
                auth_token_json = json.loads(response.read().decode("utf-8"))

                # Validate response contains accessToken
                if not auth_token_json or "accessToken" not in auth_token_json:
                    raise TokenManagerError("Access token not received from API")

                return auth_token_json["accessToken"]

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_body)
                error_msg = error_json.get("message", error_json.get("error", str(e)))
                raise TokenManagerError(f"API Error (HTTP {e.code}): {error_msg}")
            except json.JSONDecodeError:
                raise TokenManagerError(f"API Error (HTTP {e.code}): {error_body}")

        except urllib.error.URLError as e:
            raise TokenManagerError(f"Network Error: {str(e)}")

        except TokenManagerError:
            raise
        except Exception as e:
            raise TokenManagerError(f"Failed to fetch authentication token: {str(e)}")

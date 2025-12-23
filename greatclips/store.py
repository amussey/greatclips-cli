"""Store-related CLI commands for Great Clips API."""

import json
import sys
import click

from greatclips.api.stylewaretouch_api import (
    get_wait_times,
    APIError
)
from greatclips.api.webservices_api import (
    search_stores_by_term,
    search_stores_by_point,
    search_stores_by_rect,
    WebservicesAPIError
)
from greatclips.api.auth.token_manager import TokenManager, TokenManagerError
from greatclips.utils.display import display_wait_times, display_search_results


@click.group()
def store():
    """Store-related commands."""
    pass


@store.command(name='wait-times')
@click.argument('store_numbers', nargs=-1, type=int, required=True)
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def store_wait_times(store_numbers, output_json):
    """
    Get wait times for one or more stores.

    Example: greatclips-cli store wait-times 8874 8875 8876
    """
    try:
        result = get_wait_times(list(store_numbers))

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            display_wait_times(result)

    except APIError as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        raise click.Exit(1)


@store.command(name='search-term')
@click.argument('term', type=str, required=True)
@click.option('--token', type=str, default=None, help='Great Clips API access token (auto-generated if not provided)')
@click.option('--radius', type=int, default=50, help='Search radius in miles (default: 50)')
@click.option('--limit', type=int, default=50, help='Max results (default: 50)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def store_search_term(term, token, radius, limit, output_json):
    """
    Search for stores by term (zip code, city name, etc).

    Example: greatclips-cli store search-term "60601"
    Example: greatclips-cli store search-term "Boston" --radius 25
    """
    try:
        # Generate token if not provided
        if not token:
            click.echo("Generating authentication token...", err=True)
            token_manager = TokenManager()
            token = token_manager.fetch_token()

        result = search_stores_by_term(
            term=term,
            radius=radius,
            limit=limit,
            access_token=token
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            display_search_results(result)

    except TokenManagerError as e:
        click.secho(f"Token Error: {str(e)}", fg='red', err=True)
        sys.exit(1)
    except WebservicesAPIError as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)


@store.command(name='search-point')
@click.option('--lat', type=float, required=True, help='Latitude')
@click.option('--lng', type=float, required=True, help='Longitude')
@click.option('--token', type=str, default=None, help='Great Clips API access token (auto-generated if not provided)')
@click.option('--radius', type=int, default=50, help='Search radius in miles (default: 50)')
@click.option('--limit', type=int, default=50, help='Max results (default: 50)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def store_search_point(lat, lng, token, radius, limit, output_json):
    """
    Search for stores near a coordinate (latitude, longitude).

    Example: greatclips-cli store search-point --lat 41.8781 --lng -87.6298
    """
    try:
        # Generate token if not provided
        if not token:
            click.echo("Generating authentication token...", err=True)
            token_manager = TokenManager()
            token = token_manager.fetch_token()

        result = search_stores_by_point(
            latitude=lat,
            longitude=lng,
            radius=radius,
            limit=limit,
            access_token=token
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            display_search_results(result)

    except TokenManagerError as e:
        click.secho(f"Token Error: {str(e)}", fg='red', err=True)
        sys.exit(1)
    except WebservicesAPIError as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)


@store.command(name='search-rect')
@click.option('--lat1', type=float, required=True, help='Latitude of first corner')
@click.option('--lng1', type=float, required=True, help='Longitude of first corner')
@click.option('--lat2', type=float, required=True, help='Latitude of second corner')
@click.option('--lng2', type=float, required=True, help='Longitude of second corner')
@click.option('--token', type=str, default=None, help='Great Clips API access token (auto-generated if not provided)')
@click.option('--radius', type=int, default=50, help='Search radius in miles (default: 50)')
@click.option('--limit', type=int, default=50, help='Max results (default: 50)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def store_search_rect(lat1, lng1, lat2, lng2, token, radius, limit, output_json):
    """
    Search for stores within a rectangular area (map bounds).

    Example: greatclips-cli store search-rect --lat1 41.9 --lng1 -87.7 --lat2 41.8 --lng2 -87.6
    """
    try:
        # Generate token if not provided
        if not token:
            click.echo("Generating authentication token...", err=True)
            token_manager = TokenManager()
            token = token_manager.fetch_token()

        result = search_stores_by_rect(
            lat1=lat1,
            lng1=lng1,
            lat2=lat2,
            lng2=lng2,
            radius=radius,
            limit=limit,
            access_token=token
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            display_search_results(result)

    except TokenManagerError as e:
        click.secho(f"Token Error: {str(e)}", fg='red', err=True)
        sys.exit(1)
    except WebservicesAPIError as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)

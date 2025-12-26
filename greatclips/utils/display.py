"""Display utilities for formatting CLI output."""

import click


def display_wait_times(data):
    """Format and display wait times in human-readable format."""
    if isinstance(data, list):
        for store in data:
            display_store_info(store)
    else:
        display_store_info(data)


def display_store_info(store):
    """Display a single store's wait time information."""
    store_num = store.get("storeNumber", "N/A")
    wait_time = store.get("estimatedWaitMinutes", -1)
    state_code = store.get("ociSalonStateCode", "N/A")
    state_desc = store.get("ociSalonStateDescription", "Unknown")

    click.echo(f"\nStore #{store_num}")
    click.echo(f"  Status: {state_desc} ({state_code})")

    if wait_time >= 0:
        click.echo(f"  Wait Time: {wait_time} minutes")
    else:
        click.echo(f"  Wait Time: Unavailable")


def display_search_results(data):
    """Format and display search results in human-readable format."""
    if isinstance(data, dict) and "salonData" in data:
        salons = data.get("salonData", [])
    elif isinstance(data, list):
        salons = data
    else:
        salons = [data]

    if not salons:
        click.secho("No stores found", fg="yellow")
        return

    click.secho(f"Found {len(salons)} store(s):", fg="green")
    for salon in salons:
        display_search_result(salon)


def display_search_result(salon):
    """Display a single search result."""
    store_num = salon.get("salonNumber", "N/A")
    name = salon.get("marketingSalonName", "Unknown")
    address = salon.get("primaryAddress", "")
    distance = salon.get("distance", "N/A")
    wait_time = salon.get("estimatedWaitTimeMinutes", -1)
    status = salon.get("statusDescription", "Unknown")

    click.echo(f"\nStore #{store_num}")
    click.echo(f"  Name: {name}")
    if address:
        click.echo(f"  Address: {address}")
    if distance != "N/A":
        click.echo(f"  Distance: {distance} miles")
    click.echo(f"  Status: {status}")
    if wait_time >= 0:
        click.echo(f"  Wait Time: {wait_time} minutes")

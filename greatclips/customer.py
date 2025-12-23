"""Customer-related CLI commands for Great Clips API."""

import json
import click

from greatclips.api.stylewaretouch_api import (
    check_in_customer,
    cancel_check_in,
    get_customer_status,
    APIError
)


@click.group()
def customer():
    """Customer-related commands."""
    pass


@customer.command(name='check-in')
@click.option('--store', type=int, required=True, help='Store number')
@click.option('--name', type=str, required=True, help='Customer name')
@click.option('--phone', type=str, required=True, help='Phone number')
@click.option('--guests', type=int, default=1, help='Number of guests')
@click.option('--ip', type=str, default='', help='IP address')
@click.option('--profile-id', type=str, default='', help='Profile ID')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def customer_check_in(store, name, phone, guests, ip, profile_id, output_json):
    """
    Check a customer in to a salon.

    Example: greatclips-cli customer check-in --store 8874 --name "John Doe" --phone "555-1234"
    """
    try:
        result = check_in_customer(
            store_number=store,
            name=name,
            phone=phone,
            guests=guests,
            ip_address=ip,
            profile_id=profile_id
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            click.secho("✓ Check-in successful!", fg='green')
            click.echo(json.dumps(result, indent=2))

    except APIError as e:
        click.secho(f"✗ Check-in failed: {str(e)}", fg='red', err=True)
        raise click.Exit(1)


@customer.command(name='cancel')
@click.option('--oci-id', type=str, required=True, help='OCI ID from check-in')
@click.option('--store', type=int, required=True, help='Store number')
@click.option('--phone', type=str, required=True, help='Phone number')
@click.option('--guests', type=int, default=1, help='Number of guests')
@click.option('--ip', type=str, default='', help='IP address')
@click.option('--name', type=str, default='', help='Customer name')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def customer_cancel(oci_id, store, phone, guests, ip, name, output_json):
    """
    Cancel a customer's check-in.

    Example: greatclips-cli customer cancel --oci-id ABC123 --store 8874 --phone "555-1234"
    """
    try:
        result = cancel_check_in(
            oci_id=oci_id,
            store_number=store,
            phone=phone,
            guests=guests,
            ip_address=ip,
            name=name
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            click.secho("✓ Cancellation successful!", fg='green')
            click.echo(json.dumps(result, indent=2))

    except APIError as e:
        click.secho(f"✗ Cancellation failed: {str(e)}", fg='red', err=True)
        raise click.Exit(1)


@customer.command(name='status')
@click.option('--oci-id', type=str, required=True, help='OCI ID from check-in')
@click.option('--store', type=int, required=True, help='Store number')
@click.option('--phone', type=str, required=True, help='Phone number')
@click.option('--guests', type=int, default=1, help='Number of guests')
@click.option('--ip', type=str, default='', help='IP address')
@click.option('--profile-id', type=str, default='', help='Profile ID')
@click.option('--name', type=str, default='', help='Customer name')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def customer_status(oci_id, store, phone, guests, ip, profile_id, name, output_json):
    """
    Get the status of a customer's check-in.

    Example: greatclips-cli customer status --oci-id ABC123 --store 8874 --phone "555-1234"
    """
    try:
        result = get_customer_status(
            oci_id=oci_id,
            store_number=store,
            phone=phone,
            guests=guests,
            ip_address=ip,
            profile_id=profile_id,
            name=name
        )

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            click.secho("✓ Status retrieved!", fg='green')
            click.echo(json.dumps(result, indent=2))

    except APIError as e:
        click.secho(f"✗ Status request failed: {str(e)}", fg='red', err=True)
        raise click.Exit(1)

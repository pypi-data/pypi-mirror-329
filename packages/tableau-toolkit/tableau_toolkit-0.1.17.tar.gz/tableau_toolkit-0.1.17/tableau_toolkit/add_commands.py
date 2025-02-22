import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate
from .cli_utils import get_csv_data


@click.group()
def add():
    """Add various Tableau resources"""


@add.command()
@click.option("--site-name", required=True, help="Name of the site to add users to")
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.pass_context
def users(ctx, site_name, file, stdin, delimiter):
    """Add users to a specified Tableau site"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        # Find the site
        all_sites, _ = server.sites.get()
        site = next((site for site in all_sites if site.name == site_name), None)
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return

        # Switch to the specified site
        server.auth.switch_site(site)

        csv_data = get_csv_data(file, stdin, delimiter)

        for row in csv_data:
            username = row.get("object_name")
            full_name = row.get("object_full_name")
            email = row.get("object_email")
            site_role = row.get("site_role_name", "Viewer")
            auth_setting = row.get("auth_setting", "ServerDefault")

            if not username or not email:
                click.echo("Skipping row: username and email are required fields")
                continue

            try:
                new_user = TSC.UserItem(username, site_role, auth_setting)
                new_user.email = email
                new_user.fullname = full_name
                server.users.add(new_user)
                click.echo(f"Successfully added user: {username}")
            except TSC.ServerResponseError as e:
                click.echo(f"Error adding user {username}: {str(e)}", err=True)

    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"Unexpected error: {str(e)}", err=True)
    finally:
        server.auth.sign_out()

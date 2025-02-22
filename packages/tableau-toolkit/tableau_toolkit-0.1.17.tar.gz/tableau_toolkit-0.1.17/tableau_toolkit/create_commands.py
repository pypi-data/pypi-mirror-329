import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate


@click.group()
def create():
    """Clone various Tableau resources"""


@create.command()
@click.option("--site-name", help="Site Name to create")
@click.pass_context
def site(
    ctx,
    site_name,
):
    """Create a site"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        # Create a new site
        new_site = TSC.SiteItem(name=f"{site_name}", content_url=f"{site_name}")
        new_site = server.sites.create(new_site)
    except TSC.ServerResponseError as e:
        click.echo(
            f"Error creating site {site_name}: {str(e)}",
            err=True,
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()

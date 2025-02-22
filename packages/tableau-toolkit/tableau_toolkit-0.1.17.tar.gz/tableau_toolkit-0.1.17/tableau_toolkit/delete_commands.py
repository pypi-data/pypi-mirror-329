from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import csv
import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate
from .cli_utils import get_csv_data
from .logging_config import configure_logging, get_logger
from .exception_handler import exception_handler

# Configure logging for this module
configure_logging(output_dir="output", module_name=__name__)
logger = get_logger(__name__)


@click.group()
def delete():
    """Delete various Tableau resources"""


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site LUID", help="Column name for Site LUID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option("--task-id-col", default="Task LUID", help="Column name for Task LUID")
@click.option(
    "--task-name-col", default="Schedule Name", help="Column name for Task Name"
)
@click.option(
    "--content-type-col", default="Content Type", help="Column name for Content Type"
)
@click.option(
    "--content-name-col", default="Content Name", help="Column name for Content Name"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def tasks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    task_id_col,
    task_name_col,
    content_type_col,
    content_name_col,
    owner_name_col,
):
    """Delete Tableau tasks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}
    csv_data = get_csv_data(file, stdin, delimiter)

    for row in csv_data:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        task_id = row[task_id_col]
        task_name = row[task_name_col]
        site_name = row[site_name_col]
        content_type = row[content_type_col]
        content_name = row[content_name_col]
        owner_name = row[owner_name_col]

        try:
            server.auth.switch_site(site)
            server.tasks.delete(task_id)
            click.echo(
                f"Successfully deleted task: {task_name} "
                f"(ID: {task_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Content: {content_type} - {content_name}")
            click.echo(f"Owner: {owner_name}")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting task {task_name} " f"(ID: {task_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--workbook-id-col", default="Workbook ID", help="Column name for Workbook ID"
)
@click.option(
    "--workbook-name-col", default="Workbook Name", help="Column name for Workbook Name"
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def workbooks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    workbook_id_col,
    workbook_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau workbooks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        csv_data = sys.stdin
    elif file:
        with open(file, "r", encoding="utf-8", newline="") as csv_file:
            csv_data = csv.DictReader(csv_file, delimiter=delimiter)
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        workbook_id = row[workbook_id_col]
        workbook_name = row[workbook_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.workbooks.delete(workbook_id)
            click.echo(
                f"Successfully deleted workbook: {workbook_name} "
                f"(ID: {workbook_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting workbook {workbook_name} "
                f"(ID: {workbook_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--datasource-id-col", default="Datasource ID", help="Column name for Datasource ID"
)
@click.option(
    "--datasource-name-col",
    default="Datasource Name",
    help="Column name for Datasource Name",
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def datasources(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    datasource_id_col,
    datasource_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau datasources specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        csv_data = sys.stdin
    elif file:
        with open(file, "r", encoding="utf-8", newline="") as csv_file:
            csv_data = csv.DictReader(csv_file, delimiter=delimiter)

    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        datasource_id = row[datasource_id_col]
        datasource_name = row[datasource_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.datasources.delete(datasource_id)
            click.echo(
                f"Successfully deleted datasource: {datasource_name} "
                f"(ID: {datasource_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting datasource {datasource_name} "
                f"(ID: {datasource_id}): {str(e)}",
                err=True,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()

@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option(
    "--user-luid-col", default="object_luid", help="Column name for User LUID"
)
@click.option("--site-luid-col", default="site_luid", help="Column name for Site LUID")
@click.option(
    "--threads", default=1, type=int, help="Number of concurrent threads for updates"
)
@click.pass_context
def users(
    ctx,
    file,
    stdin,
    delimiter,
    user_luid_col,
    site_luid_col,
    threads,
):
    """Delete Tableau users specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    csv_data = get_csv_data(file, stdin, delimiter)

   # Group data by site
    site_groups = defaultdict(list)
    for row in csv_data:
        site_luid = row[site_luid_col]
        site_groups[site_luid].append(row)


    @exception_handler
    def delete_user(server: TSC.Server, site, user_luid):
        try:
            server.users.remove(user_luid)
            logger.info(
                "User deleted",
                user_luid=user_luid,
                site_name=site.name,
                site_id=site.id,
            )
            return f"Removed user ({user_luid}) on site {site.name} ({site.id})"
        except (TSC.ServerResponseError, ValueError, TypeError, AttributeError) as e:
            logger.error("Error removing user", user_luid=user_luid, error=str(e))
            return f"Error removing user {user_luid}: {str(e)}"

    for site_luid, site_data in site_groups.items():
        try:
            site = next(
                (site for site in TSC.Pager(server.sites) if site.id == site_luid), None
            )
            if not site:
                logger.error("Site not found", site_luid=site_luid)
                continue

            server.auth.switch_site(site)
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [
                    executor.submit(
                        delete_user,
                        server,
                        site,
                        row[user_luid_col],
                    )
                    for row in site_data
                ]

                for future in as_completed(futures):
                    result = future.result()
                    logger.info(result)
        except (ValueError, TypeError, AttributeError) as e:
            logger.exception(f"Error processing site: {e}", site_luid=site_luid)

    server.auth.sign_out()


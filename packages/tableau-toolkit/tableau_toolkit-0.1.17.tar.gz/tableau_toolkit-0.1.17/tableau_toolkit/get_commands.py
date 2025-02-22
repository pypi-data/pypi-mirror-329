import click
from .cli_utils import execute_get_query
from .cli_utils import load_config
from .cli_utils import authenticate
from .cli_utils import Projects

from .queries.view_queries import get_views_query
from .queries.workbook_queries import get_workbooks_query
from .queries.datasource_queries import get_datasources_query
from .queries.extract_refresh_queries import get_extract_refreshes_query

from .queries.subscription_queries import get_subscriptions_query
from .queries.data_alert_queries import get_data_alerts_query

from .queries.customized_view_queries import get_customized_views_query
from .queries.user_queries import get_users_query
from .queries.group_queries import get_groups_query

from .logging_config import configure_logging, get_logger
import tableauserverclient as TSC
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, TableDefinition, SqlType, Inserter, escape_name
import psycopg2  # Changed this import
from psycopg2 import sql
from psycopg2.extras import DictCursor
import json

# Configure logging for this module
configure_logging(output_dir="output", module_name=__name__)
logger = get_logger(__name__)

@click.group()
def get():
    """Get various Tableau resources"""


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def customized_views(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
):
    """Get customized views with usage data"""
    query = get_customized_views_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)

@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def workbooks(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
):
    """Get workbooks with usage data"""
    query = get_workbooks_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option("--luid", default=None, help="Filter by object luid")
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def datasources(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    luid,
    columns,
    output_hyper,
):
    """Get datasources with usage data"""
    query = get_datasources_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
        "luid": luid,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)

@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="content_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def extract_refreshes(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
):
    """Get extract refreshes with usage data"""
    query = get_extract_refreshes_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="content_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def subscriptions(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
):
    """Get subscriptions with usage data"""
    query = get_subscriptions_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)

@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def data_alerts(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
):
    """Get data alerts with usage data"""
    query = get_data_alerts_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "owner_username": owner_username,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)


@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_username", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option("--username", default=None, help="Filter by user name (system_user.name)")
@click.option("--exclude-unlicensed", is_flag=True, help="Exclude unlicensed users")
@click.option("--exclude-guest", is_flag=True, help="Exclude guest users")
@click.option("--exclude-system-admin-auto", is_flag=True, help="Exclude auto system admin users")
@click.option("--exclude-has-email", is_flag=True, help="Exclude has email")
@click.option(
    "--only-inactive-180d",
    default=False,
    is_flag=True,
    help="Include only users inactive for 180 days",
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def users(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    username,
    exclude_unlicensed,
    exclude_guest,
    exclude_system_admin_auto,
    exclude_has_email,
    only_inactive_180d,
    columns,
    output_hyper,
):
    """Get users with usage data"""
    query = get_users_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "username": username,
        "exclude_unlicensed": exclude_unlicensed,
        "exclude_guest": exclude_guest,
        "exclude_system_admin_auto": exclude_system_admin_auto,
        "exclude_has_email": exclude_has_email,
        "only_inactive_180d": only_inactive_180d,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)

@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--site-admin-username",
    default=None,
    help="Filter by site admin name (system_user.name)",
)
@click.option(
    "--exclude-grant-license-mode",
    default=False,
    is_flag=True,
    help="Filter by site admin name (system_user.name)",
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.pass_context
def groups(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    site_admin_username,
    exclude_grant_license_mode,
    columns,
    output_hyper,
):
    """Get groups with usage data"""
    query = get_groups_query()
    params = {
        "headers": headers,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "preview": preview,
        "site_name": site_name,
        "site_admin_username": site_admin_username,
        "exclude_grant_license_mode": exclude_grant_license_mode,
    }
    execute_get_query(ctx, query, params, header_map, columns, output_hyper)

@get.command()
@click.option(
    "--header-map",
    default=None,
    help='JSON string to map column names, e.g. \'{"site_name":"Site Name"}\'',
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--sort-by", default="object_name", help="Column to sort by")
@click.option(
    "--sort-order",
    default="desc",
    type=click.Choice(["asc", "desc"]),
    help="Sort order",
)
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--preview/--no-preview",
    default=False,
    help="Print the query instead of executing it",
)
@click.option("--site-name", default=None, help="Filter by site name")
@click.option(
    "--owner-username", default=None, help="Filter by owner username (system_user.name)"
)
@click.option(
    "--columns", help="Comma-separated list of columns to return", default=None
)
@click.option(
    "--output-hyper",
    default=None,
    help="Path to output .hyper file. If specified, results are written to the .hyper file instead of stdout.",
)
@click.option(
    "--api-type",
    default="rest",
    type=click.Choice(["repository", "rest"]),
    help="API type to use for fetching views",
)
@click.pass_context
def views(
    ctx,
    header_map,
    headers,
    sort_by,
    sort_order,
    limit,
    preview,
    site_name,
    owner_username,
    columns,
    output_hyper,
    api_type,
):
    """Get views with usage data"""
    if api_type == "repository":
        query = get_views_query()
        params = {
            "headers": headers,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "limit": limit,
            "preview": preview,
            "site_name": site_name,
            "owner_username": owner_username,
        }
        execute_get_query(ctx, query, params, header_map, columns, output_hyper)
    else:  # api_type == "rest"
        config = load_config(ctx.obj["config"])
        server = authenticate(config)

        try:
            # all_sites, _ = server.sites.get()
            current_site = next((site for site in TSC.Pager(server.sites) if site.id == server.site_id), None)

            # Check if we need to switch sites
            if site_name is not None and site_name != current_site.content_url:
                new_site = next((site for site in TSC.Pager(server.sites) if site.content_url == site_name), None)
                if new_site:
                    server.auth.switch_site(new_site)
                    logger.info(f"Switched to site: {new_site.name}")
                else:
                    logger.warning(f"Site with content_url '{site_name}' not found. Using current site.")

            # Load projects for generating full project path later
            projects = Projects()
            projects.populate_from_server(server)
            public_url = config['tableau_server']['public_url']

            # Load workbooks
            workbooks = {workbook.id: {'workbook_name': workbook.name} for workbook in TSC.Pager(server.workbooks)}

            view_data = []
            for view in TSC.Pager(server.views):
                full_path = projects.get_full_path(view.project_id, delimiter='/')

                if site_name and site_name != "":
                    link = f"{public_url}/#/site/{site_name}/views/{view.content_url.replace('/sheets/', '/')}"
                else:
                    link = f"{public_url}/#/views/{view.content_url.replace('/sheets/', '/')}"

                view_data.append({
                    'object_name': view.name,
                    'workbook_name': workbooks[view.workbook_id]['workbook_name'] if view.workbook_id in workbooks else None,
                    'project_path': full_path,
                    'view_link': link,
                })

            # Sort and limit results
            view_data.sort(key=lambda x: x[sort_by], reverse=(sort_order == "desc"))
            view_data = view_data[:limit]

            # Print results
            if headers:
                print("\t".join(view_data[0].keys()))
            for row in view_data:
                print("\t".join(str(v) for v in row.values()))

        except Exception as e:
            logger.error(f"Error fetching views: {str(e)}")
        finally:
            server.auth.sign_out()
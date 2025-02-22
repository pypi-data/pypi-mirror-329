import os
import click
import tableauserverclient as TSC
from .cli_utils import load_config
from .cli_utils import authenticate


@click.group()
def download():
    """Download various Tableau resources"""


@download.command()
@click.option(
    "--site-name", default="Default", help="Name of the site containing the workbook"
)
@click.option(
    "--project-name",
    default="",
    help="Name of the project containing the workbook",
)
@click.option("--workbook-name", required=True, help="Name of the workbook to download")
@click.option("--output-path", default=".", help="Path to save the downloaded workbook")
@click.pass_context
def workbook(ctx, site_name, project_name, workbook_name, output_path):
    """Download a Tableau workbook"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        # Switch to the specified site
        site = next(
            (site for site in TSC.Pager(server.sites) if site.name == site_name), None
        )
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        # Find the workbook
        req_option = TSC.RequestOptions()
        req_option.filter.add(
            TSC.Filter(
                TSC.RequestOptions.Field.Name,
                TSC.RequestOptions.Operator.Equals,
                workbook_name,
            )
        )

        if project_name:
            req_option.filter.add(
                TSC.Filter(
                    TSC.RequestOptions.Field.ProjectName,
                    TSC.RequestOptions.Operator.Equals,
                    project_name,
                )
            )
        matching_workbooks = list(TSC.Pager(server.workbooks, req_option))

        if not matching_workbooks:
            click.echo(
                f"Workbook '{workbook_name}' not found in project '{project_name}'",
                err=True,
            )
            return

        wb = matching_workbooks[0]

        # Download the workbook
        output_filename = f"{workbook_name}.twbx"
        output_path = os.path.join(output_path, output_filename)
        server.workbooks.download(wb.id, output_path)
        click.echo(f"Workbook downloaded successfully: {output_path}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"Error downloading workbook: {str(e)}", err=True)
    finally:
        server.auth.sign_out()


@download.command()
@click.option(
    "--site-name", default="Default", help="Name of the site containing the flow"
)
@click.option(
    "--project-name", default="", help="Name of the project containing the flow"
)
@click.option("--flow-name", required=True, help="Name of the flow to download")
@click.option("--output-path", default=".", help="Path to save the downloaded flow")
@click.pass_context
def flow(ctx, site_name, project_name, flow_name, output_path):
    """Download a Tableau flow"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        site = next(
            (site for site in TSC.Pager(server.sites) if site.name == site_name), None
        )
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        req_option = TSC.RequestOptions()
        req_option.filter.add(
            TSC.Filter(
                TSC.RequestOptions.Field.Name,
                TSC.RequestOptions.Operator.Equals,
                flow_name,
            )
        )

        if project_name:
            req_option.filter.add(
                TSC.Filter(
                    TSC.RequestOptions.Field.ProjectName,
                    TSC.RequestOptions.Operator.Equals,
                    project_name,
                )
            )
        matching_flows = list(TSC.Pager(server.flows, req_option))

        if not matching_flows:
            click.echo(
                f"Flow '{flow_name}' not found in project '{project_name}'", err=True
            )
            return

        f = matching_flows[0]

        output_filename = f"{flow_name}.tfl"
        output_path = os.path.join(output_path, output_filename)
        server.flows.download(f.id, output_path)
        click.echo(f"Flow downloaded successfully: {output_path}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"Error downloading flow: {str(e)}", err=True)
    finally:
        server.auth.sign_out()


## Download Datasource Command


@download.command()
@click.option(
    "--site-name", default="Default", help="Name of the site containing the datasource"
)
@click.option(
    "--project-name",
    default="",
    help="Name of the project containing the datasource",
)
@click.option(
    "--datasource-name", required=True, help="Name of the datasource to download"
)
@click.option(
    "--output-path", default=".", help="Path to save the downloaded datasource"
)
@click.pass_context
def datasource(ctx, site_name, project_name, datasource_name, output_path):
    """Download a Tableau datasource"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    try:
        site = next(
            (site for site in TSC.Pager(server.sites) if site.name == site_name), None
        )
        if not site:
            click.echo(f"Site '{site_name}' not found", err=True)
            return
        server.auth.switch_site(site)

        req_option = TSC.RequestOptions()
        req_option.filter.add(
            TSC.Filter(
                TSC.RequestOptions.Field.Name,
                TSC.RequestOptions.Operator.Equals,
                datasource_name,
            )
        )

        if project_name:
            req_option.filter.add(
                TSC.Filter(
                    TSC.RequestOptions.Field.ProjectName,
                    TSC.RequestOptions.Operator.Equals,
                    project_name,
                )
            )
        matching_datasources = list(TSC.Pager(server.datasources, req_option))

        if not matching_datasources:
            click.echo(
                f"Datasource '{datasource_name}' not found in project '{project_name}'",
                err=True,
            )
            return

        ds = matching_datasources[0]

        output_filename = f"{datasource_name}.tdsx"
        output_path = os.path.join(output_path, output_filename)
        server.datasources.download(ds.id, output_path)
        click.echo(f"Datasource downloaded successfully: {output_path}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"Error downloading datasource: {str(e)}", err=True)
    finally:
        server.auth.sign_out()

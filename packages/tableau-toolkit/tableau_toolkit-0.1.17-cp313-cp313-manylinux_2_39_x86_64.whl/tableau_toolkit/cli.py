import base64
import io
from pathlib import Path
import csv
from tableauhyperapi import (
    HyperProcess,
    Connection,
    SqlType,
    TableDefinition,
    Telemetry,
    CreateMode,
    Inserter,
)
import click
import yaml
from .cli_utils import get_default_config_path
from .get_commands import get
from .create_commands import create
from .delete_commands import delete
from .download_commands import download
from .update_commands import update
from .add_commands import add


@click.group()
@click.option(
    "--config", default=get_default_config_path(), help="Path to the configuration file"
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


# Add the command groups to the main CLI
cli.add_command(get)
cli.add_command(create)
cli.add_command(delete)
cli.add_command(download)
cli.add_command(update)
cli.add_command(add)


# Other top-level commands
@cli.command()
def init():
    """Initialize the tableau_toolkit configuration."""
    home_dir = Path.home()
    config_dir = home_dir / ".tableau_toolkit"
    config_file = config_dir / "tableau.yaml"

    if config_file.exists():
        click.echo("Configuration file already exists. Do you want to overwrite it?")
        if not click.confirm("Overwrite?"):
            click.echo("Initialization cancelled.")
            return

    config_dir.mkdir(exist_ok=True)

    default_config = {
        "tableau_server": {"url": "https://hostname", "public_url": "https://hostname"},
        "authentication": {"type": "tableau_auth"},
        "personal_access_token": {"name": "name", "secret": "secret", "secret_encoded": True},
        "tableau_auth": {"username": "username", "password": "password", "password_encoded": True},
        "site": {"content_url": ""},
        "api": {"version": "3.24"},
        "postgres": {
            "host": "host",
            "port": 8060,
            "dbname": "workgroup",
            "user": "readonly",
            "password": "password",
            "password_encoded": True,
        },
    }

    with config_file.open("w") as f:
        yaml.dump(default_config, f, default_flow_style=False)

    click.echo(f"Configuration file created at {config_file}")


@cli.command()
@click.argument("string")
def encode(string):
    """Encode a string using Base64 encoding."""
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    click.echo(encoded_str)


@cli.command()
@click.argument("encoded_string")
def decode(encoded_string):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_str = decoded_bytes.decode("utf-8")
        click.echo(decoded_str)
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding string: {e}")


@cli.command()
@click.option(
    "--input",
    "-i",
    type=click.File("r"),
    default="-",
    help="Input CSV file (default: stdin)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=True, dir_okay=False),
    default="output/db.hyper",
    help="Output Hyper file",
)
@click.option(
    "--table-name", default="extract", help="Name of the table in the Hyper file"
)
@click.option(
    "--schema-map", type=click.File("r"), help="JSON file containing schema mapping"
)
@click.option(
    "--mode",
    type=click.Choice(["create", "append"]),
    default="create",
    help="Mode to open the Hyper file",
)
@click.option(
    "--delimiter", default="\t", help="Delimiter for the input data (default: tab)"
)
def load(input, output, table_name, schema_map, mode, delimiter):
    """Load data from CSV or stdin into a Hyper file."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read all input data into memory
    input_data = input.read()

    # Create two separate CSV readers
    schema_reader = csv.reader(io.StringIO(input_data), delimiter=delimiter)
    data_reader = csv.reader(io.StringIO(input_data), delimiter=delimiter)

    # Read schema map if provided
    if schema_map:
        import json

        schema = json.load(schema_map)
    else:
        # Infer schema from the first row of CSV
        sample = next(schema_reader)
        schema = {col: SqlType.text() for col in sample}

    # Define the table structure
    table_def = TableDefinition(
        table_name=table_name,
        columns=[TableDefinition.Column(name, type) for name, type in schema.items()],
    )

    # Start Hyper process
    with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        # Use `CREATE_IF_NOT_EXISTS` to create the Hyper file if it doesn't exist
        with Connection(
            endpoint=hyper.endpoint,
            database=output_path,
            create_mode=CreateMode.CREATE_IF_NOT_EXISTS,
        ) as connection:
            if mode == "create":
                # Drop the table if it exists
                if connection.catalog.has_table(table_def.table_name):
                    click.echo(
                        f"Table '{table_name}' exists. Dropping and re-creating it..."
                    )
                    connection.execute_command(f"DROP TABLE IF EXISTS {table_name}")

                # Create the table
                connection.catalog.create_table(table_def)

            elif mode == "append":
                # Create the table if it does not exist
                if not connection.catalog.has_table(table_def.table_name):
                    click.echo(f"Table '{table_name}' does not exist. Creating it...")
                    connection.catalog.create_table(table_def)

            # Load data
            next(data_reader)  # Skip the header row
            data = [row for row in data_reader]
            with Inserter(connection, table_def) as inserter:
                inserter.add_rows(rows=data)
                inserter.execute()

    click.echo(f"Data loaded into table '{table_name}' at {output_path}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()

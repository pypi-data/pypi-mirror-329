import csv
import sys
import base64
from pathlib import Path
import json
import yaml
import tableauserverclient as TSC
import click
from tableauhyperapi import HyperProcess, Nullability, Telemetry, Connection, CreateMode, TableDefinition, SqlType, Inserter, escape_name
from .logging_config import get_logger 
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import traceback

logger = get_logger(__name__)  # Get the logger instance

CONFIG_FILE = str(Path.home().joinpath(".tableau_toolkit", "tableau.yaml"))


def get_csv_data(file, stdin, delimiter):
    if stdin:
        return csv.DictReader(sys.stdin, delimiter=delimiter)
    if file:

        def csv_generator(file, delimiter):
            def generate():
                with open(file, "r", encoding="ISO-8859-1", newline="") as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=delimiter)
                    yield from reader

            return generate()

        return csv_generator(file, delimiter)
    raise click.UsageError("Either --file or --stdin must be provided")


def get_default_config_path():
    return str(Path.home() / CONFIG_FILE)


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def decode_secret(encoded_secret):
    decoded_bytes = base64.b64decode(encoded_secret.split(":")[0])
    return decoded_bytes.decode("utf-8")


def authenticate(config) -> TSC.Server:
    server_url = config["tableau_server"]["url"]
    site_content_url = config["site"]["content_url"]
    api_version = config["api"]["version"]

    if config["authentication"]["type"] == "personal_access_token":
        token_name = config["personal_access_token"]["name"]
        secret_encoded = config["personal_access_token"].get("secret_encoded", True)  

        if secret_encoded:
            token_secret = decode_secret(config["personal_access_token"]["secret"])
        else:
            token_secret = config["personal_access_token"]["secret"]

        tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name, token_secret, site_id=site_content_url
        )
    else:
        username = config["tableau_auth"]["username"]
        password_encoded = config["tableau_auth"].get("password_encoded", True)  

        if password_encoded:
            password = decode_secret(config["tableau_auth"]["password"])
        else:
            password = config["tableau_auth"]["password"]
        
        tableau_auth = TSC.TableauAuth(username, password, site_id=site_content_url)

    server = TSC.Server(server_url, use_server_version=False)
    server.add_http_options({"verify": False})
    server.version = api_version
    server.auth.sign_in(tableau_auth)
    return server

def execute_get_query(ctx, query, params, header_map=None, columns=None, output_hyper=None):
    config = load_config(ctx.obj["config"])
    params["tableau_server_url"] = config["tableau_server"]["public_url"]
    formatted_query = query.format(
        sort_column=sql.Identifier(params["sort_by"]),
        sort_direction=sql.SQL(params["sort_order"].upper()),
        tableau_server_url=sql.SQL(params["tableau_server_url"]),
    )

    password_encoded = config["postgres"].get("password_encoded", True)

    if password_encoded:
        password = decode_secret(config["postgres"]["password"])
    else:
        password = config["postgres"]["password"]

    postgres_config = {
        "dbname": config["postgres"]['dbname'],
        "host": config["postgres"]['host'],
        "port": config["postgres"]['port'],
        "user": config["postgres"]['user'],
        "password": password,
    }

    if params["preview"]:
        click.echo("Query to be executed:")
        with psycopg2.connect(**postgres_config) as conn:
            with conn.cursor() as cur:
                query_string = cur.mogrify(formatted_query, params)
                click.echo(query_string)
    else:
        try:
            with psycopg2.connect(**postgres_config) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:  # Use DictCursor
                    cur.execute(formatted_query, params)

                    # Get column names from cursor description
                    column_names = [desc[0] for desc in cur.description]

                    if columns:
                        selected_columns = [x.strip() for x in columns.split(",")]
                    else:
                        selected_columns = column_names

                    # validate selected columns
                    invalid_columns = [
                        col for col in selected_columns if col not in column_names
                    ]
                    if invalid_columns:
                        raise ValueError(f"Invalid columns specified: {invalid_columns}")

                    if header_map:
                        mapping = json.loads(header_map)
                        display_headers = [
                            mapping.get(col, col) for col in selected_columns
                        ]
                    else:
                        display_headers = selected_columns

                    results = cur.fetchall() #fetch all rows

                    if output_hyper:
                        try:
                            with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                                with Connection(hyper.endpoint, output_hyper, CreateMode.CREATE_AND_REPLACE) as connection:
                                    table_name = "Extract"  # You can customize the table name
                                    table_definition = TableDefinition(table_name)

                                    # Infer Types from psycopg cursor description
                                    for desc in cur.description:
                                        column_name = desc[0]
                                        column_type = desc[1]

                                        if column_name not in selected_columns:
                                            continue  # Skip columns not selected
                                        sql_type = SqlType.text()  # Default to TEXT for unknown types

                                        table_definition.add_column(column_name, sql_type, nullability=Nullability.NULLABLE)

                                    connection.catalog.create_table(table_definition)

                                    with Inserter(connection, table_definition) as inserter:
                                        for row in results:
                                            # Prepare data for insertion, handling potential None values
                                            row_values = []
                                            for col in selected_columns:
                                                value = row[col]  # Access by name
                                                if value is None:
                                                    row_values.append(None)
                                                else:
                                                    row_values.append(str(value))
                                            inserter.add_row(row_values)
                                        inserter.execute()
                            logger.info(f"Results written to .hyper file: {output_hyper}")

                        except Exception as e:
                            logger.error(f"Error writing to .hyper file: {traceback.format_exc()}")
                    else:
                        if params["headers"]:
                            click.echo("\t".join(display_headers))

                        for row in results:
                            click.echo(
                                "\t".join(
                                    (
                                        str(row[col]).replace("\n", "\\n").replace("\t", "\\t")
                                        if row[col] is not None
                                        else ""
                                    )
                                    for col in selected_columns
                                )
                            )
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise  # Re-raise the exception so the CLI user sees it

def get_full_project_path(server, project):
    pass

class Projects:
    def __init__(self):
        self.project_dict = {}

    def add_project(self, project_id, name, parent_id=None):
        
        # Ensure the project itself is initialized
        if project_id not in self.project_dict:
            self.project_dict[project_id] = {
                'name': name,
                'parent_id': parent_id,
                'children': [],
            }
        else:
            self.project_dict[project_id].update({'name': name, 'parent_id': parent_id})

        # Ensure parent_id exists before adding children
        if parent_id:
            if parent_id not in self.project_dict:
                self.project_dict[parent_id] = {
                    'name': None,  # Placeholder, can be updated later
                    'parent_id': None,
                    'children': [],
                }
            self.project_dict[parent_id]['children'].append(project_id)

    def get_full_path(self, project_id, delimiter='/'):
        path = []
        current_id = project_id
        while current_id is not None:
            if current_id not in self.project_dict:
                break
            project = self.project_dict[current_id]
            path.insert(0, project['name'])
            current_id = project['parent_id']
        return delimiter.join(path)
    
    def populate_from_server(self, server: TSC.Server):
        for project in TSC.Pager(server.projects):
            self.add_project(project.id, project.name, project.parent_id)
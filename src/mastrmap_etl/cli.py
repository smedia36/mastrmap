import click

from .extract import fetch_from_url
from .transform import csv_to_geodf
from .load import to_geopackage, to_postgis


@click.group()
def cli():
    """CLI for the MSDR ETL scaffold."""


@cli.command()
@click.option("--source", required=True, help="URL to download (CSV or ZIP)")
@click.option("--out", default="data", help="Output directory")
def fetch(source, out):
    path = fetch_from_url(source, out)
    click.echo(f"Downloaded: {path}")


@cli.command(name="transform")
@click.option("--in", "in_path", required=True, help="Input CSV path")
@click.option("--out", "out_path", default="data/msdr.gpkg", help="Output geopackage path")
@click.option("--layer", default="msdr", help="Layer name in geopackage")
def transform_cmd(in_path, out_path, layer):
    gdf = csv_to_geodf(in_path)
    to_geopackage(gdf, out_path, layer=layer)
    click.echo(f"Wrote geopackage: {out_path}")


@cli.command(name="load-postgis")
@click.option("--in", "in_path", required=True, help="Input CSV path")
@click.option("--db-url", required=True, help="SQLAlchemy DB URL for PostGIS")
@click.option("--table", default="msdr", help="Destination table name")
def load_postgis_cmd(in_path, db_url, table):
    gdf = csv_to_geodf(in_path)
    to_postgis(gdf, db_url, table_name=table)
    click.echo(f"Loaded to PostGIS table: {table}")


if __name__ == "__main__":
    cli()

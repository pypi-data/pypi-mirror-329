"""Command-line interface for reading GeoParquet files."""

import sys
from pathlib import Path

import click
import geopandas as gpd


@click.group()
@click.version_option()
def cli():
    """Simple tool for reading GeoParquet files."""
    pass


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('-n', '--limit', type=int, default=5, help='Number of rows to display')
def read(filepath, limit):
    """Read and display a GeoParquet file."""
    try:
        gdf = gpd.read_parquet(filepath)
        click.echo(f"Successfully read GeoParquet file with {len(gdf)} rows")
        click.echo(f"CRS: {gdf.crs}")
        click.echo(f"Geometry column: {gdf._geometry_column_name}")
        click.echo(f"Columns: {', '.join(gdf.columns)}")
        click.echo("\nFirst {limit} rows:")
        click.echo(gdf.head(limit))
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def info(filepath):
    """Display basic information about a GeoParquet file."""
    try:
        gdf = gpd.read_parquet(filepath)
        click.echo(f"Rows: {len(gdf)}")
        click.echo(f"Columns: {len(gdf.columns)}")
        click.echo(f"CRS: {gdf.crs}")
        click.echo(f"Geometry types: {gdf.geometry.geom_type.value_counts().to_dict()}")
        click.echo(f"Bounds: {gdf.total_bounds.tolist()}")
        
        # Display column information
        click.echo("\nColumns:")
        for col in gdf.columns:
            click.echo(f"  - {col} ({gdf[col].dtype})")
            
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

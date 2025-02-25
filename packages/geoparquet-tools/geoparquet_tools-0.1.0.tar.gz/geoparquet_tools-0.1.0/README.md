# geoparquet-tools

A simple command-line tool for reading GeoParquet files.

## Installation

```bash
pip install geoparquet-tools
```

## Usage

```bash
# Display information about a GeoParquet file
geoparq info path/to/file.parquet

# Read and display rows from a GeoParquet file
geoparq read path/to/file.parquet

# Show the first 10 rows
geoparq read path/to/file.parquet --limit 10
```

## Requirements

- Python 3.7+
- geopandas
- pyarrow
- click

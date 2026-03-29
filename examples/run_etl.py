"""Example runner for the MSDR ETL scaffold."""
from mastrmap_etl import fetch_from_url, csv_to_geodf, to_geopackage


MSDR_URL = "https://example.com/msdr_dump.zip"  # replace with real URL


def run_example():
    csv_path = fetch_from_url(MSDR_URL, out_dir="data")
    gdf = csv_to_geodf(csv_path)
    out = to_geopackage(gdf, "data/msdr.gpkg")
    print("Wrote:", out)


if __name__ == "__main__":
    run_example()

import os


def to_geopackage(gdf, path: str, layer: str = "msdr") -> str:
    """Write GeoDataFrame to a GeoPackage file.

    Returns the path written.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    gdf.to_file(path, layer=layer, driver="GPKG")
    return path


def to_postgis(gdf, engine_url: str, table_name: str = "msdr", if_exists: str = "replace") -> None:
    """Load GeoDataFrame into PostGIS using SQLAlchemy/GeoAlchemy2."""
    from sqlalchemy import create_engine

    engine = create_engine(engine_url)
    # geopandas >=0.10 exposes to_postgis
    gdf.to_postgis(table_name, engine, if_exists=if_exists, index=False)

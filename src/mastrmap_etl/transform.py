import pandas as pd
import geopandas as gpd
import shapely.wkt as wkt


def csv_to_geodf(csv_path: str, lon_col: str = "longitude", lat_col: str = "latitude", wkt_col: str = None, crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    """Load a CSV and return a cleaned GeoDataFrame.

    The function attempts the following in order:
    - use `wkt_col` if provided
    - use `lon_col`/`lat_col` if present
    - try to auto-detect lon/lat-like columns
    """
    df = pd.read_csv(csv_path, dtype=str, low_memory=False)

    if wkt_col and wkt_col in df.columns:
        df["geometry"] = df[wkt_col].apply(lambda s: wkt.loads(s) if pd.notnull(s) else None)
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=crs)

    elif lon_col in df.columns and lat_col in df.columns:
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")
        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs)

    else:
        # attempt heuristic detection
        possible_lon = [c for c in df.columns if "lon" in c.lower() or "lng" in c.lower()]
        possible_lat = [c for c in df.columns if "lat" in c.lower()]
        if possible_lon and possible_lat:
            return csv_to_geodf(csv_path, lon_col=possible_lon[0], lat_col=possible_lat[0], wkt_col=wkt_col, crs=crs)
        raise ValueError("No coordinate columns found in CSV and no WKT column provided")

    # basic cleaning
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]
    # drop exact-duplicate rows (excluding geometry) to reduce duplicates
    non_geom = [c for c in gdf.columns if c != gdf.geometry.name]
    if non_geom:
        gdf = gdf.drop_duplicates(subset=non_geom)
    return gdf

from fused._optional_deps import (
    GPD_GEODATAFRAME,
    HAS_GEOPANDAS,
    HAS_MERCANTILE,
    HAS_SHAPELY,
    MERCANTILE_TILE,
    SHAPELY_GEOMETRY,
)


def estimate_zoom(bounds) -> int:
    """
    Estimate the zoom level for a given bounding box.

    This method returns the zoom level at which a tile exists that, potentially
    shifted slightly, fully covers the bounding box.

    Args:
        bounds: A list of 4 coordinates (minx, miny, maxx, maxy), a
            GeoDataFrame or Shapely geometry, or a mercantile Tile.

    Returns:
        The estimated zoom level (0-20).

    """
    if HAS_GEOPANDAS and isinstance(bounds, GPD_GEODATAFRAME):
        bounds = bounds.total_bounds
    elif HAS_SHAPELY and isinstance(bounds, SHAPELY_GEOMETRY):
        bounds = bounds.bounds
    elif HAS_MERCANTILE and isinstance(bounds, MERCANTILE_TILE):
        return bounds.z
    elif not isinstance(bounds, list):
        raise TypeError(f"Invalid bounds type: {type(bounds)}")

    if not HAS_MERCANTILE:
        raise ImportError("This function requires the mercantile package.")
    import mercantile

    minx, miny, maxx, maxy = bounds

    centroid = (minx + maxx) / 2, (miny + maxy) / 2
    width = (maxx - minx) - 1e-11
    height = (maxy - miny) - 1e-11

    for z in range(20, 0, -1):
        tile = mercantile.tile(*centroid, zoom=z)
        west, south, east, north = mercantile.bounds(tile)
        if width <= (east - west) and height <= (north - south):
            break

    return z

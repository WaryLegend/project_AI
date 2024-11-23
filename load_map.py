import geopandas as gpd

def load_vietnam_map(shapefile_path):
    return gpd.read_file(shapefile_path)

def filter_southern_provinces(vietnam, provinces):
    return vietnam[vietnam['NAME_1'].isin(provinces)].to_crs(epsg=3857)  # Chuyển sang hệ tọa độ phẳng
    
import geojson
import folium
from seavoyage.classes.m_network import MNetwork

def map_folium(
    geojson_data: dict | geojson.FeatureCollection, 
    center: tuple[float, float] = (36.0, 129.5), 
    zoom: int = 7,
    ) -> folium.Map:
    m = folium.Map(location=center, zoom_start=zoom)
    
    folium.GeoJson(geojson_data, name="GeoJSON Layer").add_to(m)
    return m

def map_folium_marnet(
    marnet: MNetwork,
    center: tuple[float, float] = (36.0, 129.5),
    zoom: int = 7,
) -> folium.Map:
    m = folium.Map(location=center, zoom_start=zoom)
    folium.GeoJson(marnet.to_geojson(), name="GeoJSON Layer").add_to(m)
    return m

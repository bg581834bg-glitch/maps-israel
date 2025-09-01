import folium

# קואורדינטות ירושלים
center_lat, center_lon = 31.77, 35.21

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=8,
    tiles=None
)

# שכבת אריחים לזום 8-10 (הגדרת minZoom=8, maxZoom=10)
folium.TileLayer(
    tiles='http://localhost:8000/tiles/{z}/{x}/{y}.png',
    attr='Local Tiles',
    name='Local Tiles',
    minZoom=7,
    maxZoom=14,
    overlay=False,
    control=True
).add_to(m)

folium.LayerControl().add_to(m)
from folium.plugins import MeasureControl
m.add_child(MeasureControl())
folium.Marker([31.77, 35.21], popup="ירושלים").add_to(m)
from folium.plugins import MiniMap
minimap = MiniMap()
m.add_child(minimap)


m.save('local_tiles_jerusalem.html')

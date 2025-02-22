import requests
from IPython.display import display
from PIL import Image
from io import BytesIO

def get_map(longitude, latitude, map_style="streets-v11", zoom=12, width=600, height=400):
    """
    Fetches a static map image from Mapbox API.
    
    Parameters:
        longitude (float): Longitude of the location.
        latitude (float): Latitude of the location.
        map_style (str): Mapbox map style (default: "streets-v11").
        zoom (int): Zoom level (default: 12).
        width (int): Width of the image in pixels (default: 600).
        height (int): Height of the image in pixels (default: 400).
    """
    mapbox_access_token = "pk.eyJ1IjoiYWxiZXJ0cGFtb25hZyIsImEiOiJjbDJsa3d1M3kwb2VtM2Nwa2Vxajd1MDdsIn0.GQx5HParNf5Ba4AngkoBAw"
    
    url = (f"https://api.mapbox.com/styles/v1/mapbox/{map_style}/static/"
           f"{longitude},{latitude},{zoom}/{width}x{height}"
           f"?access_token={mapbox_access_token}")
    
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        display(image)
    else:
        print("Error fetching map image:", response.json())

# Example usage
# get_map(120.9842, 14.5995)

#!/usr/bin/env python3
"""
Download OpenStreetMap tiles for Massachusetts, New Hampshire, and Vermont
"""

import os
import requests
import time
import math
from urllib.parse import urljoin

def deg2num(lat_deg, lon_deg, zoom):
    """Convert lat/lon to tile numbers"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x = int((lon_deg + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (x, y)

def download_tile(x, y, z, base_dir="tiles"):
    """Download a single tile"""
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    tile_dir = os.path.join(base_dir, str(z), str(x))
    os.makedirs(tile_dir, exist_ok=True)
    tile_path = os.path.join(tile_dir, f"{y}.png")
    
    # Skip if already exists
    if os.path.exists(tile_path):
        return True
    
    try:
        headers = {
            'User-Agent': 'Meshtastic Logger Tile Downloader 1.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        with open(tile_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {z}/{x}/{y}")
        time.sleep(0.1)  # Be nice to OSM servers
        return True
        
    except Exception as e:
        print(f"Failed to download {z}/{x}/{y}: {e}")
        return False

def download_region_tiles(north, south, east, west, min_zoom=6, max_zoom=14):
    """Download tiles for a geographic region"""
    print(f"Downloading tiles for region: N{north}, S{south}, E{east}, W{west}")
    print(f"Zoom levels: {min_zoom} to {max_zoom}")
    
    total_tiles = 0
    downloaded_tiles = 0
    
    for zoom in range(min_zoom, max_zoom + 1):
        # Calculate tile bounds for this zoom level
        # Top-left corner (northwest)
        x_min, y_min = deg2num(north, west, zoom)
        # Bottom-right corner (southeast) 
        x_max, y_max = deg2num(south, east, zoom)
        
        # Ensure proper bounds and order
        if x_min > x_max:
            x_min, x_max = x_max, x_min
        if y_min > y_max:
            y_min, y_max = y_max, y_min
            
        x_min = max(0, x_min)
        x_max = min(2**zoom - 1, x_max)
        y_min = max(0, y_min)
        y_max = min(2**zoom - 1, y_max)
        
        zoom_tiles = (x_max - x_min + 1) * (y_max - y_min + 1)
        total_tiles += zoom_tiles
        
        print(f"Zoom {zoom}: {zoom_tiles} tiles ({x_max-x_min+1}x{y_max-y_min+1}) - X:{x_min}-{x_max}, Y:{y_min}-{y_max}")
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if download_tile(x, y, zoom):
                    downloaded_tiles += 1
                
                # Progress update every 100 tiles
                if downloaded_tiles % 100 == 0:
                    print(f"Progress: {downloaded_tiles}/{total_tiles} tiles")
    
    print(f"Download complete: {downloaded_tiles}/{total_tiles} tiles")

def main():
    """Download tiles for MA, NH, and VT"""
    # Approximate bounding boxes for the states
    regions = {
        "Massachusetts": {
            "north": 42.887,
            "south": 41.237,
            "east": -69.858,
            "west": -73.508
        },
        "New Hampshire": {
            "north": 45.307,
            "south": 42.697,
            "east": -70.610,
            "west": -72.557
        },
        "Vermont": {
            "north": 45.013,
            "south": 42.726,
            "east": -71.465,
            "west": -73.354
        }
    }
    
    # Combined bounding box for all three states
    combined = {
        "north": max(r["north"] for r in regions.values()),
        "south": min(r["south"] for r in regions.values()),
        "east": max(r["east"] for r in regions.values()),
        "west": min(r["west"] for r in regions.values())
    }
    
    print("Downloading tiles for MA, NH, and VT combined region...")
    print(f"Combined bounds: N{combined['north']:.3f}, S{combined['south']:.3f}, E{combined['east']:.3f}, W{combined['west']:.3f}")
    
    # Create tiles directory
    os.makedirs("tiles", exist_ok=True)
    
    # Download tiles (zoom 6-12 for reasonable download size)
    download_region_tiles(
        north=combined["north"],
        south=combined["south"], 
        east=combined["east"],
        west=combined["west"],
        min_zoom=6,
        max_zoom=12
    )

if __name__ == "__main__":
    main()
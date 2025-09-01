import os
import math
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def latlon_to_tile(lat, lon, zoom):
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n)
    return x, y

def download_tile(z, x, y, save_dir):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyOfflineMap/1.0; +https://yourdomain.com)"
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            os.makedirs(f"{save_dir}/{z}/{x}", exist_ok=True)
            with open(f"{save_dir}/{z}/{x}/{y}.png", "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed: {url} ({response.status_code})")
    except Exception as e:
        print(f"Error: {url} ({e})")

# גבולות ישראל (בערך)
min_lat, max_lat = 29.5, 33.5
min_lon, max_lon = 34.2, 35.9
zoom = 14

x_min, y_max = latlon_to_tile(min_lat, min_lon, zoom)
x_max, y_min = latlon_to_tile(max_lat, max_lon, zoom)

tasks = []
for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        tasks.append((zoom, x, y, "tiles"))

# הגבל ל-4 חוטים (אפשר לשנות ל-2-8)
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(download_tile, *task) for task in tasks]
    for future in as_completed(futures):
        pass  # אפשר להוסיף הדפסה או טיפול בשגיאות כאן

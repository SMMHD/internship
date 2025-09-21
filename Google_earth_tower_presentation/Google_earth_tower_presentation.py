import os
import re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import simplekml
import tkinter as tk
from tkinter import filedialog

# Function to extract EXIF data
def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if not info:
        return exif_data
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]
            exif_data["GPSInfo"] = gps_data
    return exif_data

# Function to convert GPS coordinates to decimal format
def convert_to_degrees(value):
    if isinstance(value, tuple):
        d, m, s = value
        d = float(d) if hasattr(d, '__float__') else d[0]/d[1]
        m = float(m) if hasattr(m, '__float__') else m[0]/m[1]
        s = float(s) if hasattr(s, '__float__') else s[0]/s[1]
        return d + m/60 + s/3600
    return None

# Function to extract latitude and longitude
def get_lat_lon(exif_data):
    gps_info = exif_data.get("GPSInfo", {})
    if not gps_info:
        return None, None

    lat = gps_info.get("GPSLatitude")
    lat_ref = gps_info.get("GPSLatitudeRef")
    lon = gps_info.get("GPSLongitude")
    lon_ref = gps_info.get("GPSLongitudeRef")

    if lat and lon and lat_ref and lon_ref:
        lat = convert_to_degrees(lat)
        if lat is None:
            return None, None
        if lat_ref != "N":
            lat = -lat
        lon = convert_to_degrees(lon)
        if lon is None:
            return None, None
        if lon_ref != "E":
            lon = -lon
        return lat, lon
    return None, None

# Function to extract tower number from folder name
def get_tower_number(folder_name):
    # Support for TOWER (number) format with optional space
    match = re.search(r'TOWER \s*\((\d+)\)', folder_name)
    return int(match.group(1)) if match else None

# Function to find the parent TOWER folder name
def get_tower_parent_name(root_path):
    while root_path != os.path.dirname(root_path):  # Avoid infinite loop at root
        parent_name = os.path.basename(root_path)
        if get_tower_number(parent_name) is not None:
            return parent_name
        root_path = os.path.dirname(root_path)
    return None

# Function to create KMZ file by processing one image from each TOWER subfolder
def create_kmz_from_images(root_folder, kmz_filename):
    kml = simplekml.Kml()
    towers = []  # List to store (tower_number, name, lat, lon) tuples

    # Define style for custom icon
    style = simplekml.Style()
    style.iconstyle.icon.href = "transmission-tower.png"  # Path to custom icon file
    style.iconstyle.scale = 1.0  # Icon size
    style.iconstyle.color = simplekml.Color.blue  # Blue color for icon

    # Traverse all subfolders recursively
    for root, dirs, files in os.walk(root_folder):
        image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg"))]
        if image_files:
            first_image = image_files[0]
            filepath = os.path.join(root, first_image)
            try:
                image = Image.open(filepath)
                exif_data = get_exif_data(image)
                lat, lon = get_lat_lon(exif_data)
                if lat and lon:
                    # Use the parent TOWER folder name instead of the immediate subfolder
                    tower_name = get_tower_parent_name(root)
                    if tower_name:
                        tower_number = get_tower_number(tower_name)
                        if tower_number is not None:
                            # Check if tower with this number already exists to avoid duplicates
                            if not any(t[0] == tower_number for t in towers):
                                towers.append((tower_number, tower_name, lat, lon))
                                print(f"Added: {tower_name}/{first_image} ({lat}, {lon})")
                            else:
                                print(f"Skipped duplicate tower: {tower_name}/{first_image}")
                        else:
                            print(f"Invalid tower name format: {tower_name}/{first_image}")
                    else:
                        print(f"No valid TOWER parent folder found for: {root}/{first_image}")
                else:
                    print(f"No GPS data: {os.path.basename(root)}/{first_image}")
            except Exception as e:
                print(f"Error reading {os.path.basename(root)}/{first_image}: {e}")

    # Sort towers by tower number
    towers.sort(key=lambda x: x[0])

    # Add points to KML (only unique towers)
    for tower_number, name, lat, lon in towers:
        if lat is not None and lon is not None:  # Ensure valid coordinates
            pnt = kml.newpoint(name=name, coords=[(lon, lat)])
            pnt.style = style

    # Create a single continuous line connecting all towers with valid coordinates
    if len(towers) > 1:
        tower_coords = [(lon, lat) for _, _, lat, lon in towers if lat is not None and lon is not None]
        if tower_coords:  # Only create line if there are valid coordinates
            ls = kml.newlinestring(name="Tower Path")
            ls.coords = tower_coords
            ls.style.linestyle.color = simplekml.Color.blue
            ls.style.linestyle.width = 2
            ls.style.polystyle.fill = 0

    # Save KMZ file
    kml.savekmz(kmz_filename)
    print(f"\nKMZ file created: {kmz_filename}")

# Create UI for selecting folder and output file
def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open folder selection dialog
    print("Please select the folder containing TOWER images...")
    folder_path = filedialog.askdirectory(title="Select TOWER Folder")
    if not folder_path:
        print("No folder selected. Program will exit.")
        return

    # Open save file dialog for KMZ
    print("Please select the path and name for the output KMZ file...")
    kmz_filename = filedialog.asksaveasfilename(
        title="Save KMZ File",
        defaultextension=".kmz",
        filetypes=[("KMZ files", "*.kmz")]
    )
    if not kmz_filename:
        print("No file selected for saving. Program will exit.")
        return

    # Run the main function with selected paths
    create_kmz_from_images(folder_path, kmz_filename)

if __name__ == "__main__":
    main()
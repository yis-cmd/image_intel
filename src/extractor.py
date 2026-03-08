import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A
"""


def dms_to_decimal(dms_tuple, ref):
    if not dms_tuple or not ref:
        return None
    try:
        degrees = float(dms_tuple[0])
        minutes = float(dms_tuple[1])
        seconds = float(dms_tuple[2])

        decimal = degrees + minutes / 60 + seconds / 3600
        if ref in [b'S', b'W', 'S', 'W']:
            decimal = -decimal
        return decimal
    except Exception:
        return None


def has_gps(data: dict):
    return "GPSInfo" in data


def latitude(data: dict):
    if has_gps(data):
        gps_info = data["GPSInfo"]
        gps_data = {GPSTAGS.get(k, k): v for k, v in gps_info.items()}
        return dms_to_decimal(gps_data.get('GPSLatitude'), gps_data.get('GPSLatitudeRef'))
    return None


def longitude(data: dict):
    if has_gps(data):
        gps_info = data["GPSInfo"]
        gps_data = {GPSTAGS.get(k, k): v for k, v in gps_info.items()}
        return dms_to_decimal(gps_data.get('GPSLongitude'), gps_data.get('GPSLongitudeRef'))
    return None


def datatime(data: dict):
    return (
        data.get("DateTimeOriginal")
        or data.get("DateTimeDigitized")
        or data.get("DateTime")
    )


def camera_make(data: dict):
    return data.get("Make")


def camera_model(data: dict):
    return data.get("Model")


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת ובונה את המילון הסופי.
    """
    path = Path(image_path)

    try:
        img = Image.open(image_path)
        exif_raw = img._getexif()
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        exif_raw = None

    if exif_raw is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    # המרת ה-IDs לשמות של תגיות (Make, Model וכו')
    data = {}
    for tag_id, value in exif_raw.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    return {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }


def extract_all(folder_path):
    all_images = []
    if not os.path.exists(folder_path):
        print(f"התיקייה {folder_path} לא קיימת.")
        return all_images


    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            all_images.append(extract_metadata(full_path))

    return all_images
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_metadata(image_path: str) -> dict:

    result = {
        "filename": os.path.basename(image_path),
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    }

    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return result

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "DateTime":
                result["datetime"] = value
            elif tag_name == "Make":
                result["camera_make"] = value
            elif tag_name == "Model":
                result["camera_model"] = value
            elif tag_name == "GPSInfo":
                result["has_gps"] = True
                gps_data = {}
                for key, val in value.items():
                    gps_tag_name = GPSTAGS.get(key, key)
                    gps_data[gps_tag_name] = val
                latitude = gps_data['GPSLatitude']
                longitude = gps_data['GPSLongitude']
                la_ref = gps_data['GPSLatitudeRef']
                lo_ref = gps_data['GPSLongitudeRef']
                def dms_to_decimal(dms_tuple, ref):
                    degrees = dms_tuple[0][0] / dms_tuple[0][1]
                    minutes = dms_tuple[1][0] / dms_tuple[1][1]
                    seconds = dms_tuple[2][0] / dms_tuple[2][1]
                    decimal = degrees + minutes / 60 + seconds / 3600
                    if ref in [b'S', b'W', 'S', 'W']:
                        decimal = -decimal
                    return decimal
                result['latitude'] = dms_to_decimal(latitude, la_ref)
                result['longitude'] = dms_to_decimal(longitude, lo_ref)
    except Exception as e:
        print(f"Error reading {image_path}: {e}")

    return result

def extract_all(folder_path: str) -> list[dict]:

    all_images = []

    if not os.path.exists(folder_path):
        print(f"התיקייה {folder_path} לא קיימת.")
        return all_images

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('JPEG'):
            full_path = os.path.join(folder_path, filename)
            image_metadata = extract_metadata(full_path)
            all_images.append(image_metadata)

    return all_images

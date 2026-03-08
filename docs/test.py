def dms_to_decimal(dms_tuple, ref):
    degrees = dms_tuple[0][0] / dms_tuple[0][1]
    minutes = dms_tuple[1][0] / dms_tuple[1][1]
    seconds = dms_tuple[2][0] / dms_tuple[2][1]
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in [b'S', b'W', 'S', 'W']:
        decimal = -decimal
    return decimal

print(dms_to_decimal(((32, 1), (5, 1), (7, 1)), 's'))

from PIL import Image
from PIL.ExifTags import TAGS


def test_exif(image_path):
    # פותחים את התמונה
    image = Image.open(image_path)

    # שולפים את המידע הגולמי
    exif_data = image.getexif()

    if not exif_data:
        print("לא נמצאו נתוני EXIF בתמונה הזו.")
        return

    # עוברים על הנתונים ומתרגמים את המזהים המספריים לשמות מובנים
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        print(f"{tag_name}: {value}")


# שים פה נתיב לתמונה שיש לך על המחשב
test_exif("my_test_image.jpg")
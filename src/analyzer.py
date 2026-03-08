from datetime import datetime

def analyze(images_data: list[dict]) -> dict:
    """
    מנתח את הנתונים ומוצא דפוסים.
    
    מקבל: רשימת מילונים מ-extract_all
    מחזיר: מילון עם תובנות, לדוגמה:
    {
        "total_images": 12,
        "images_with_gps": 10,
        "unique_cameras": ["Samsung Galaxy S23", "Apple iPhone 15 Pro"],
        "date_range": {"start": "2025-01-12", "end": "2025-01-16"},
        "insights": [
            "נמצאו 3 מכשירים שונים",
            "הסוכן החליף מכשיר ב-13/01",
            "ריכוז תמונות באזור תל אביב"
        ]
    }
    """

    if not images_data:
        return {}

    img_num = len(images_data)
    img_with_gps = len([img for img in images_data if img.get('has_gps')])

    sorted_data = sorted(images_data, key=lambda x: x.get('datetime', ''))
    start_date = sorted_data[0]['datetime']
    end_date = sorted_data[-1]['datetime']

    cameras = {f"{img.get('camera_make', 'Unknown')} {img.get('camera_model', '')}".strip() 
               for img in images_data if img.get('camera_make')}
    
    insights = []
    
    if len(cameras) > 1:
        insights.append(f"נמצאו {len(cameras)} מכשירים שונים בשימוש.")

    last_cam = None
    for img in sorted_data:
        current_cam = f"{img.get('camera_make')} {img.get('camera_model')}"
        if last_cam and current_cam != last_cam:
            change_date = img['datetime'].split(' ')[0]
            insights.append(f"זוהה שינוי במכשיר ב- {change_date} (מ-{last_cam} ל-{current_cam})")
            break 
        last_cam = current_cam

    if img_with_gps > 0:
        insights.append(f"{img_with_gps} תמונות מכילות נתוני מיקום גיאוגרפיים.")
    else:
        insights.append("אזהרה: לא נמצאו נתוני GPS באף אחת מהתמונות.")

    return {
        "total_images": img_num,
        "images_with_gps": img_with_gps,
        "unique_cameras": list(cameras),
        "date_range": {
            "start": start_date.split(' ')[0], 
            "end": end_date.split(' ')[0]
        },
        "insights": insights
    }

if __name__ == "__main__":
    fake_data:list[dict] = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    a = analyze(fake_data)
    print(a)
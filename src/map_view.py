"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium
from datetime import datetime

def sort_by_time(arr:list[dict])->list[dict]:
    return sorted(arr, key=lambda x: datetime.fromisoformat(x['datetime']))


def create_map(images_data:list[dict])->str:
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [
    img for img in images_data
    if img.get("has_gps") and img.get("latitude") and img.get("longitude")
    ]
    gps_images = sort_by_time(gps_images)
    
    if not gps_images:
        return "<h1>No GPS data available</h1>"
    

    avg_lat = sum(img['latitude'] for img in gps_images) / len(gps_images)
    avg_lon = sum(img['longitude'] for img in gps_images) / len(gps_images)
    
    interactive_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred']
    device_colors = {}
    color_index = 0

    for img in gps_images:
        model = img.get("camera_model", "Unknown")
        if model not in device_colors:
            device_colors[model] = colors[color_index % len(colors)]
            color_index += 1

        folium.Marker(
            location=[img['latitude'], img['longitude']],
            popup=f"File: {img['filename']}<br>Time: {img['datetime']}",
            tooltip=f"Device: {model}",
            icon=folium.Icon(color=device_colors[model], icon="info-sign")
        ).add_to(interactive_map)

    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: auto; 
                border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
                padding: 10px; opacity: 0.8;">
        <strong>Devices</strong><br>
    '''
    for model, color in device_colors.items():
        legend_html += f'<span><i style="background:{color}; width:10px; height:10px; display:inline-block;"></i> {model}</span><br>'
    legend_html += '</div>'
    
    interactive_map.get_root().html.add_child(folium.Element(legend_html))

    return interactive_map._repr_html_()


if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data:list[dict] = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
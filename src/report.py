from jinja2 import Environment, FileSystemLoader


def create_report(images_data: list[dict], map_html: str, 
                  timeline_html: str, analysis: dict) -> str:
    """
    מרכיב את כל החלקים לדו"ח HTML אחד.
    
    מקבל:
        - images_data: רשימת מילונים מ-extract_all
        - map_html: HTML של המפה מ-create_map
        - timeline_html: HTML של ציר הזמן מ-create_timeline
        - analysis: מילון התובנות מ-analyze
    מחזיר: string של HTML מלא (הדו"ח הסופי)
    """
    # example dict
    # {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
    #      "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
    #      "datetime": "2025-01-12 08:30:00"}

    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('report.html')
    return template.render(map_html=map_html, timeline_html=timeline_html, analysis=analysis)
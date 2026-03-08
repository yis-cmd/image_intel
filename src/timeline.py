import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64


def create_timeline(images_data: list[dict]) -> str:
    valid_pic = []

    for img in images_data:
        dt_s = img.get('datetime')
        if dt_s:
            dt = datetime.strptime(dt_s, '%Y:%m:%d %H:%M:%S')
            valid_pic.append({
                    'filename': img.get('filename'),
                    'datetime': dt
                })
    if not valid_pic:
        return "<div dir='rtl'><p>לא נמצאו תמונות עם נתוני זמן חוקיים ליצירת ציר זמן.</p></div>"
    valid_pic.sort(key=lambda x: x['datetime'])
    dates = [date['datetime'] for date in valid_pic]
    names = [name['filename'] for name in valid_pic]

    fig, x_line = plt.subplots(figsize=(12, 6))

    x_line.plot(dates, [0] * len(dates), "-o", color="black", markerfacecolor="cornflowerblue", markersize=10)

    for i, (date, name) in enumerate(zip(dates, names)):
        y_offset = 0.05 if i % 2 == 0 else -0.05
        va = 'bottom' if i % 2 == 0 else 'top'
        x_line.text(date, y_offset, name, rotation=45, ha='right', va=va, fontsize=9)
    x_line.get_yaxis().set_visible(False)
    x_line.spines['left'].set_visible(False)
    x_line.spines['right'].set_visible(False)
    x_line.spines['top'].set_visible(False)
    x_line.spines['bottom'].set_position('center')
    x_line.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    fig.autofmt_xdate(rotation=0, ha='center')
    plt.title('Timeline of photo shooting', pad=30, fontsize=14)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=False)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    html_string = f'''
        <div style="text-align: center; font-family: sans-serif; direction: rtl; margin: 20px;">
            <img src="data:image/png;base64,{img_base64}" alt="Timeline of Images" 
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
        </div>
        '''

    return html_string
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import extractor
import map_view
import timeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_files = request.files.getlist('photos')
    if not uploaded_files or uploaded_files[0].filename == '':
        return jsonify({"error": "לא נבחרה תיקייה או שהתיקייה ריקה"}), 400
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in uploaded_files:
                if file and file.filename:
                    # חילוץ שם הקובץ בלבד מתוך הנתיב (כדי למנוע בעיות אבטחה ונתיבים מורכבים)
                    filename = secure_filename(os.path.basename(file.filename))
                    file_path = os.path.join(temp_dir, filename)
                    file.save(file_path)

            image_data = extractor.extract_all(temp_dir)
            if not image_data:
                return jsonify({"error": "No valid images found in the specified directory."}), 404
            map_html = map_view.create_map(image_data)
            timeline_html = timeline.create_timeline(image_data)
            results = {
                "status": "success",
                "folder": "Uploaded Folder",
                "message": f"נותחו בהצלחה {len(image_data)} תמונות",
                'image_data': image_data,
                'map_html': map_html,
                'timeline_html': timeline_html
            }
            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from main import main
import io
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload-endpoint", methods=["POST"])
def upload_file():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image field in form'}), 400
    
    file = request.files['image'] #the data from javascript fetch
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        filename = secure_filename(file.filename) # guarantee safe filenames
        image_memory_buffer = io.BytesIO(file.read())

        main(image_memory_buffer)

        image_memory_buffer.close()

        # Return a JSON response with the image URL
        image_url = f"http://127.0.0.1:5000/uploads/{filename}"
        return jsonify({
            'message': 'Upload successful!',
            'imageUrl': image_url
        }), 200

@app.route('/uploads/<filename>')
def display_image(filename):
    # Sends the image file from the 'uploads' directory to the browser
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/show-data')
def show_data():
    with open('record.json', 'r') as file:
        json_data = json.load(file)

    return render_template('index.html', nutrition_data=json_data)

if __name__ == '__main__':
    # Run the server in debug mode for development
    app.run(debug=True)

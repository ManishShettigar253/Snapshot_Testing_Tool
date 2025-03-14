from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
import os
import uuid
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS for all routes with all origins allowed
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def compare_images(img1_path, img2_path):
    try:
        # Read images
        image1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

        if image1 is None or image2 is None:
            return "Error: Unable to read one or both images"

        # Resize images if they have different dimensions
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Calculate difference
        difference = cv2.absdiff(image1, image2)
        non_zero_count = np.count_nonzero(difference)
        total_pixels = image1.shape[0] * image1.shape[1]
        difference_percentage = (non_zero_count / total_pixels) * 100
        
        if difference_percentage < 0.1:  # Less than 0.1% difference
            return "Test Passed - Images are identical"
        else:
            return f"Test Failed - Images differ by {difference_percentage:.2f}%"

    except Exception as e:
        return f"Error in comparison: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['GET', 'OPTIONS'])
def ping():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        response = app.make_response("pong")
    
    # Set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
        
    try:
        print("Upload endpoint hit")
        
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Please upload both images'}), 400

        image1 = request.files['image1']
        image2 = request.files['image2']
        
        # Check if file selections are empty
        if image1.filename == '' or image2.filename == '':
            return jsonify({'error': 'No files selected'}), 400

        # Create unique filenames
        unique_id = str(uuid.uuid4())[:8]
        filename1 = secure_filename(f"{unique_id}_{image1.filename}")
        filename2 = secure_filename(f"{unique_id}_{image2.filename}")
        
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        image1.save(image1_path)
        image2.save(image2_path)
        
        print(f"Images saved to {image1_path} and {image2_path}")

        result = compare_images(image1_path, image2_path)
        print(f"Comparison result: {result}")
        
        response = jsonify({'result': result})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        print(f"Error in upload: {str(e)}")
        response = jsonify({'error': f"Server Error: {str(e)}"}), 500
        if isinstance(response, tuple):
            response[0].headers['Access-Control-Allow-Origin'] = '*'
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
        return response

if __name__ == '__main__':
    print("Server is running on http://127.0.0.1:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
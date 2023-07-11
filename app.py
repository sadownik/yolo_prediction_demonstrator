import cv2 as cv
from ultralytics import YOLO
import base64
from PIL import Image
import io
import numpy as np
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# This is your prediction function
def predict(image):
    # Convert the image to blob
    model = YOLO("yolov8n.pt") 
    results = model(image)

    return results[0].plot()

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image_file():
    if request.method == 'POST':
        f = request.files['file']
        npimg = np.fromstring(f.read(), np.uint8)
        img = cv.imdecode(npimg, cv.IMREAD_COLOR)

        prediction = predict(img)

        # Convert from BGR to RGB
        prediction_rgb = cv.cvtColor(prediction, cv.COLOR_BGR2RGB)

        # Convert numpy array to PIL Image
        prediction_pil = Image.fromarray(prediction_rgb)
        # Create in-memory bytes buffer
        byte_arr = io.BytesIO()
        # Save PIL Image to bytes buffer
        prediction_pil.save(byte_arr, format='PNG')
        # Encode as base64
        encoded_image = base64.b64encode(byte_arr.getvalue()).decode('utf-8')

        return render_template('display.html', prediction = encoded_image)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

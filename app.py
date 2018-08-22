"""
Flask Serving

This file is a sample flask app that can be used to test the model with an API.

This app does the following:
    - Handles uploads and looks for an image file send as "file" parameter
    - Stores the image at ./test dir
    - Loads the model
    - Invokes process_images function from evaluate.py with this image
    - Returns the output file generated at /output
"""

# import the necessary packages
import os
import dlib
from flask import Flask, send_file, request

# Web Server gateway Interface (WSGI) packages
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

# Utilities
from evaluate import process_images

# Admitted input file extensions
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'bmp', 'png'])

# Flask object
app = Flask(__name__)

# Decorate the Flask object with associating URL/methods with functions
@app.route('/', methods=["POST"])
def correct_rotation():
    """
    Take the input image and rotate it, if necessary
    """
    
    # check if the post request has the file part
    input_file = request.files.get('file')
    if not input_file:
        return BadRequest("File not present in request")

    # More checks
    filename = secure_filename(input_file.filename)
    if filename == '':
        return BadRequest("File name is not present in request")
    if not allowed_file(filename):
        return BadRequest("Invalid file type")

    # Save input file locally
    input_filepath = os.path.join('./test/', filename)
    output_filepath = os.path.join('./output/', filename)
    input_file.save(input_filepath)

    # initialize dlib's face detector (HOG+SVM-based)  
    detector = dlib.get_frontal_face_detector()
    
    # process the input and produce the output
    process_images(detector, input_filepath, output_filepath)

    return send_file(output_filepath, mimetype='image/jpg')

# Check if input file owns and allowed extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0')

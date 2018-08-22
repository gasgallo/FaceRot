"""
API to process face images and output the same image correctly up-down
oriented.
"""

# import the necessary packages
import argparse
import dlib
import cv2
import os

# Utilities
from utils import rotate

def process_images(detector, input_path, output_path):
    """
    Process an image iterating over 0, 90, 180, 270 degrees of rotation 
    waiting for a face to get detected. If no face is detected, then no
    output is produced.
    """

    # Admitted input file extensions
    extensions = ['.jpg', '.jpeg', '.bmp', '.png']

    # Check if input is a single image or a directory
    output_is_image = False
    if os.path.isfile(input_path):
        image_paths = [input_path]
        if os.path.splitext(output_path)[1].lower() in extensions:
            output_is_image = True
            output_filename = output_path
            output_path = os.path.dirname(output_filename)
    else:
        image_paths = [os.path.join(input_path, f) for f in
                       os.listdir(input_path)
                       if os.path.splitext(f)[1].lower() in extensions]
        if os.path.splitext(output_path)[1].lower() in extensions:
            print('Output must be a directory!')

    # Parameters
    predicted_angles = []
    out_path = []
    rotations = [0, 90, 180, 270]

    # Iteration over input images
    for path in image_paths:
        im = cv2.imread(path, 1)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Iteration over possible orientations
        for i in rotations:
            # detect faces in the grayscale frame
            faces = detector(rotate(gray, i), 0)

            # check to see if a face was detected, and if so, note the rotation
            if len(faces) > 0:
                predicted_angles.append(i)
                out_path.append(path)
                break
            
        # warn if a picture with no face is fed as an input
        if len(faces) < 1:
            print('[WARNING] No face detected in picture {}'.format(path))

    # Check output path
    if output_path == '':
        output_path = '.'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Write new images into output path
    for (path, predicted_angle) in zip(out_path, predicted_angles):
        image = cv2.imread(path)
        rotated_image = rotate(image, predicted_angle)

        if not output_is_image:
            output_filename = os.path.join(output_path,
                    os.path.basename(path))
        cv2.imwrite(output_filename, rotated_image)


if __name__ == '__main__':

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('input_path', help='path to input image')
    ap.add_argument('-o', '--output_path', help='Output directory')
    args = ap.parse_args()

    output_path = \
        (args.output_path if args.output_path else args.input_path)

    # initialize dlib's face detector (HOG+SVM-based)
    print('[INFO] Loading face detector...')
    detector = dlib.get_frontal_face_detector()

    # process the input and produce the output
    print('[INFO] Processing input image(s)...')
    process_images(detector, args.input_path, output_path)
    
    print('[INFO] Completed!')


			

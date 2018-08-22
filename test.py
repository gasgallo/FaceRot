"""
Test script to check accuracy and debug what obtained with the
evaluate.py script
"""

# import the necessary packages
import argparse
import dlib
import cv2
import os
import numpy as np

# Utilities
from utils import rotate

def test_FaceRot(detetctor, input_path):
    """
    Randomly rotates an image iterating by 0, 90, 180, 270 degrees and
    tests if the FaceRot model applys the right counter rotation.
    Finally prints the accuracy, number of not detected faces and number
    of corrupted files.
    """

    # Admitted input file extensions
    extensions = ['.jpg', '.jpeg', '.bmp', '.png']

    # Check if input is a single image or a directory
    if os.path.isfile(input_path):
        image_paths = [input_path]
    else:
        image_paths = [os.path.join(input_path, f) for f in
                       os.listdir(input_path)
                       if os.path.splitext(f)[1].lower() in extensions]

    # Parameters
    accuracy = 0.0
    count = 0
    not_det = 0
    corr = 0
    rotations = [0, 90, 180, 270]

    # Iteration over input images
    for idx, path in enumerate(image_paths):
        count += 1
        print('no {}, path {}'.format(idx,path))
        im = cv2.imread(path, 1)
        
        # If corrupted, skip
        if im is None:
            corr += 1
            count -= 1
            print('Pic {} corrupted'.format(path))
            continue
     
        # Randomly rotate pic and make it gray
        rotation_angle = np.random.choice(rotations)
        gray = cv2.cvtColor(rotate(im, rotation_angle), cv2.COLOR_BGR2GRAY)
    
        # Iteration over possible orientations
        for i in rotations:
            # detect faces in the grayscale frame
            faces = detector(rotate(gray, -i), 0)

            # check to see if a face was detected, and if so, note the rotation
            if len(faces) > 0:
                if i==rotation_angle:
                    accuracy += 1
                    print('original {}, detected {} --> GOOD'.format(rotation_angle,i))
                else:
                    print('original {}, detected {} --> BAD'.format(rotation_angle,i))
                break
        
        # If any rotation succeed, warning
        if len(faces) < 1:
            count -= 1
            not_det += 1
            print('Face not detected!')
     
    return accuracy/count, not_det, len(image_paths), corr

if __name__ == '__main__':

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('input_path', help='path to input image')
    args = ap.parse_args()

    # initialize dlib's face detector (HOG+SVM-based)
    print('[INFO] Loading face detector...')
    detector = dlib.get_frontal_face_detector()

    # process the input and produce the output
    print('[INFO] Testing accuracy...')
    acc, not_d, tot, corr = test_FaceRot(detector,args.input_path)

    print('Total number of images tested: {}'.format(tot))
    print('The accuracy on detected faces is {}%'.format(acc*100))
    print('Not detected faces: {}'.format(not_d))
    print('Corrupted pictures: {}'.format(corr))


			

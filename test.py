#!/usr/bin/python
# -*- coding: utf-8 -*-

# import the necessary packages

"""
API to process face images and output the same image correctly up-down
oriented.
"""

import argparse
import dlib
import cv2
import os
import numpy as np

from utils import rotate

def test_FaceRot(detetctor, input_path):
    """
    Randomly rotates an image iterating by 0, 90, 180, 270 degrees and
    tests if the FaceRot model applys the right counter rotation.
    Finally prints the accuracy.
    """

    extensions = ['.jpg', '.jpeg', '.bmp', '.png']

    output_is_image = False
    if os.path.isfile(input_path):
        image_paths = [input_path]
    else:
        image_paths = [os.path.join(input_path, f) for f in
                       os.listdir(input_path)
                       if os.path.splitext(f)[1].lower() in extensions]

    accuracy = 0.0
    count = 0
    not_det = 0
    corr = 0
    for idx, path in enumerate(image_paths):
	count += 1
	print('no {}, path {}'.format(idx,path))
        im = cv2.imread(path, 1)
	if im is None:
		corr += 1
		print('Pic {} corrupted'.format(path))
		break
	rotation_angle = np.random.choice([0, 90, 180, 270])
        gray = cv2.cvtColor(rotate(im, rotation_angle), cv2.COLOR_BGR2GRAY)

        for i in range(4):

        # detect faces in the grayscale frame

            faces = detector(rotate(gray, -i*90), 0)

        # check to see if a face was detected, and if so, note the rotation

            if len(faces) > 0:
                if i*90==rotation_angle:
			accuracy += 1
			print('original {}, detected {} --> GOOD'.format(rotation_angle,i*90))
		else:
			print('original {}, detected {} --> BAD'.format(rotation_angle,i*90))
                break
	    elif i==3:
		count -= 1
		not_det += 1
		print('Face not detected!')
     
    return accuracy/count, not_det, len(image_paths), corr

if __name__ == '__main__':

    # construct the argument parser and parse the arguments

    ap = argparse.ArgumentParser()
    ap.add_argument('input_path', help='path to input image')
    args = ap.parse_args()

    # initialize dlib's face detector (HOG-based)

    print('[INFO] Loading face detector...')
    detector = dlib.get_frontal_face_detector()

    # process the input and produce the output

    print('[INFO] Testing accuracy...')
    acc, not_d, tot, corr = test_FaceRot(detector,args.input_path)

    print('Total number of images tested: {}'.format(tot))
    print('The accuracy on detected faces is {}%'.format(acc*100))
    print('Not detected faces: {}'.format(not_d))
    print('Corrupted pictures: {}'.format(corr))


			

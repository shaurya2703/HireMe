### General imports ###
from __future__ import division
import numpy as np
import pandas as pd
import time
from time import sleep
import re
import os
import requests
import argparse
from collections import OrderedDict
# import ffmpeg

### Image processing ###
import cv2
from scipy.ndimage import zoom
from scipy.spatial import distance
import imutils
from scipy import ndimage
import dlib
from imutils import face_utils

### Model ###
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K


# from library.video_emotion_recognition import *
from library.text_similarity import *

import speech_recognition as sr
import moviepy.editor as mp

# import ffmpeg

def videoToText(path):


    command2mp3 = f"ffmpeg -i {path} audio.mp3"
    command2wav = "ffmpeg -i audio.mp3 audio.wav"
    

    os.system(command2mp3)
    os.system(command2wav)
    r = sr.Recognizer()
    audio = sr.AudioFile('audio.wav')

    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    os.remove('audio.mp3')
    os.remove('audio.wav')
    return result





def videoEmotion(path):
    """
    Video streaming generator function.
    """

    # Start video capute. 0 = Webcam, 1 = Video file, -1 = Webcam for Web

    video_capture = cv2.VideoCapture(path)
    # Image shape
    shape_x = 48
    shape_y = 48
    # Load the pre-trained X-Ception model
    model = load_model('Models/video.h5')

    # Load the face detector
    face_detect = dlib.get_frontal_face_detector()

    # Load the facial landmarks predictor
    predictor_landmarks = dlib.shape_predictor("Models/face_landmarks.dat")

    # Prediction vector
    predictions = []

    angry_0 = []
    disgust_1 = []
    fear_2 = []
    happy_3 = []
    sad_4 = []
    surprise_5 = []
    neutral_6 = []
    ret, frame = video_capture.read()

    # Record for 45 seconds
    while ret:

        # k = k+1
        # end = time.time()

        # Capture frame-by-frame the video_capture initiated above

        # Face index, face by face
        face_index = 0

        # Image to gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # All faces detected
        rects = face_detect(gray, 1)

        #gray, detected_faces, coord = detect_face(frame)

        # For each detected face
        for (i, rect) in enumerate(rects):

            # Identify face coordinates
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            face = gray[y:y+h, x:x+w]

            # Identify landmarks and cast to numpy
            shape = predictor_landmarks(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Zoom on extracted face
            face = zoom(
                face, (shape_x / face.shape[0], shape_y / face.shape[1]))

            # Cast type float
            face = face.astype(np.float32)

            # Scale the face
            face /= float(face.max())
            face = np.reshape(face.flatten(), (1, 48, 48, 1))

            # Make Emotion prediction on the face, outputs probabilities
            prediction = model.predict(face)

            # For plotting purposes with Altair
            angry_0.append(prediction[0][0].astype(float))
            disgust_1.append(prediction[0][1].astype(float))
            fear_2.append(prediction[0][2].astype(float))
            happy_3.append(prediction[0][3].astype(float))
            sad_4.append(prediction[0][4].astype(float))
            surprise_5.append(prediction[0][5].astype(float))
            neutral_6.append(prediction[0][6].astype(float))

            # # Most likely emotion
            prediction_result = np.argmax(prediction)

            # # Append the emotion to the final list
            predictions.append(str(prediction_result))

        cv2.imwrite('tmp/t.jpg', frame)
        cv2.imshow('Frame', frame)

        i = 0
        # print(i)
        while i < 8 and ret:
            ret, frame = video_capture.read()
            i += 1

        # Once reaching the end, write the results to the personal file and to the overall file

    print("Writing in histo_perso.txt")
    with open("static/js/db/histo_perso.txt", "w") as d:
        d.write("density"+'\n')
        for val in predictions:
            d.write(str(val)+'\n')

    with open("static/js/db/histo.txt", "a") as d:
        for val in predictions:
            d.write(str(val)+'\n')

    rows = zip(angry_0, disgust_1, fear_2, happy_3,
               sad_4, surprise_5, neutral_6)

    import csv
    with open("static/js/db/prob.csv", "w") as d:
        writer = csv.writer(d)
        for row in rows:
            writer.writerow(row)

    with open("static/js/db/prob_tot.csv", "a") as d:
        writer = csv.writer(d)
        for row in rows:
            writer.writerow(row)
    
    K.clear_session()
    
    # print(text)
    print(predictions.count('0'))
    print(len(predictions))
    final_ans = {
        0: predictions.count('0')/len(predictions),
        1: predictions.count('1')/len(predictions),
        2: predictions.count('2')/len(predictions),
        3: predictions.count('3')/len(predictions),
        4: predictions.count('4')/len(predictions),
        5: predictions.count('5')/len(predictions),
        6: predictions.count('6')/len(predictions)
        }
    print(final_ans)
    
    video_capture.release()
    cv2.destroyAllWindows()
    return final_ans,True

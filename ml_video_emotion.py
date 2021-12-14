from library.video_emotion_recognition import *
from library.text_similarity import *

import speech_recognition as sr 
import moviepy.editor as mp

def videoToText(path):
    clip = mp.VideoFileClip(path) 
 
    clip.audio.write_audiofile(r"converted.wav")

    r = sr.Recognizer()
    audio = sr.AudioFile("converted.wav")

    with audio as source:
      audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    return result

def videoEmotion(path):
    predictions = gen(path)
    # print(predictions)
    # text = videoToText(path)
    # print(text)
    return predictions

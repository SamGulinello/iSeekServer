import speech_recognition as sr
from pydub import AudioSegment

import sys
import os

class voiceDetect():

    def __init__(self):
        pass

    # method to convert a .m4a file to wav file. This is necessary for Android users
    def m4aToWav(self,fileName):
        
        (path, file_extension) = os.path.splitext(fileName)
        file_extension_final = file_extension.replace('.', '')

        track = AudioSegment.from_file(fileName, file_extension_final)

        wav_filename = fileName.replace(file_extension_final, 'wav')
        wav_path = './' + wav_filename

        file_handle = track.export(wav_path, format='wav')
        os.remove(fileName)


    # method to take in a .wav file and output text
    def wavToText(self,file):
        
        # create an instance of the speech_recognition class
        r = sr.Recognizer()

        with sr.AudioFile(file) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
        
        return text

#!/usr/bin/env python3

import speech_recognition as sr
import pandas as pd
import glob
import sys
import os

# https://realpython.com/python-speech-recognition/
def recognize(file):

    USER = # TODO get credentials from IBM

    r = sr.Recognizer()
    sound = sr.AudioFile(file)
    with sound as source:
        r.adjust_for_ambient_noise(source, duration  = 0.5)
        audio = r.record(source)
    
    transDict = r.recognize_(audio, show_all = True)
    print(transDict)
    guess = r.recognize_google(audio)
    return guess


def main():

    # Iterate over all the sound files
    typeList = ['Control', 'Diagnosed']
    for t in typeList:
        idList = list()
        guessList = list()
        # TODO needs to be CHUNKS, not Subset
        for file in glob.glob('../DATA/CHUNKS/{}/*'.format(t)):
            # TODO Check that it's WAV; if not, re-encode it to ./tmp.wav
            ext = os.path.basename(file).split('.')[-1]
            if ext == 'mp3':
                tmpSound = AudioSegment.from_mp3(file)
                tmpSound.export('./try.wav', format = 'wav')

                name = os.path.basename(file).split('.')[0]
                print('mp3')
                guess = recognize('./try.wav')
                idList.append(name)
                guessList.append(guess)

            else:
                name = os.path.basename(file).split('.')[0]
                print('wav')
                guess = recognize(file)
                idList.append(name)
                guessList.append(guess)

            print(file)
            print(idList)
            print(guessList)
            sys.exit()

        d = {'IDs': idList,
             'Transcripts': guessList
            }
        df = pd.DataFrame(d)
        print(df)
        df.to_csv('../DATA/DataFrames/{}_ASR.csv'.format(t))
        sys.exit()
            

if __name__ == "__main__":

    main()


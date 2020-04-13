#!/usr/bin/env python3

from pydub import AudioSegment # For splitting wave files into snippets
from numpy import argmax, mean, diff, log, nonzero
from scipy.signal import correlate
import soundfile as sf
import numpy as np
import parselmouth
import statistics
import shutil
import random
import glob
import math
import sys
import csv
import os


def coinToss():

    flip = random.randint(0,1)
    if flip == 0:
        return True
    else:
        return False


def send(file, length, secondsLeft, secondsCTRL, WAV=True, Diagnosed=True):

    name = os.path.basename(file)
    if WAV:
        if Diagnosed:
            dest = "../DATA/Subset/Diagnosed/{}".format(name)
            shutil.copy(file, dest)
            return secondsCTRL
        else:
            if secondsCTRL < 57415:
                coinResult = coinToss()

                if coinResult:
                    dest = "../DATA/Subset/Control/{}".format(name)
                    shutil.copy(file, dest)
                    secondsCTRL += int(length)
                    return secondsCTRL
                else:
                    return secondsCTRL
            else:
                return secondsCTRL
    else:
            
        if secondsLeft < 57412 and Diagnosed: # 57412
            coinResult = coinToss()
            if coinResult:
                dest = "../DATA/Subset/Diagnosed/{}".format(name)
                shutil.copy(file, dest)
                secondsLeft += int(length)
                return secondsLeft
            else:
                return secondsLeft
        else:
            return secondsLeft
        

def analyzeSound(sound):

    intensity = sound.get_intensity()
    numChannels = sound.get_number_of_channels()
    numSamples = sound.get_number_of_samples()
    power = sound.get_power() # sum of amplitude squared
    rms = sound.get_rms() 
    samplingFreq = sound.get_sampling_frequency()
    samplingPeri = sound.get_sampling_period()
    duration = sound.get_total_duration()
    energy = sound.get_energy()

    return (intensity, numChannels, numSamples, power, rms, samplingFreq,
            samplingPeri, duration, energy)


def doPic(dir, task, diagnosedList, secondsCTRL):

    outList = list()
    for file in glob.glob(dir + '*/*'):

        fileList = list()
        speaker = os.path.basename(file).split('.')[0].split('_')[0]

        sound = parselmouth.Sound(file)
        measures = analyzeSound(sound)

        fileList.append('Talk2Me - Picture Description')
        D = False
        for diagnosed in diagnosedList:
            if int(speaker) == diagnosed:
                fileList.append("Alzheimer's")
                D = True
                secondsCTRL = send(file, measures[-2], 1, secondsCTRL, True, True)

        if not D:
            fileList.append('Control')
            secondsCTRL = send(file, measures[-2], 1, secondsCTRL, True, False)
        fileList.append(task)
        fileList.append('WAV')
        fileList.append(speaker)
        fileList.append('False')

        for m in measures:
            fileList.append(m)

        outList.append(fileList)

    return outList, secondsCTRL


def doPPA(dir, secondsLeft):

    analysisList = list()
    outList = list()

    for file in glob.glob(dir + 'DePaul/*.mp3'):
        analysisList.append(file)
    for file in glob.glob(dir + 'Hopkins/*.mp3'):
        analysisList.append(file)

    for file in analysisList:

        fileList = list()
        speaker = os.path.basename(file).split('.')[0]
        tmpSound = AudioSegment.from_mp3(file)
        tmpSound.export('./try.wav', format = 'wav')
        sound = parselmouth.Sound('./try.wav')
        measures = analyzeSound(sound)

        fileList.append('TalkBank - PPA')
        fileList.append("Alzheimer's")
        fileList.append('Conversation')
        fileList.append('MP3')
        fileList.append(speaker)
        fileList.append('True')

        revisedSeconds = send(file, measures[-2], secondsLeft, 1, False, True)
        secondsLeft = revisedSeconds

        for m in measures:
            fileList.append(m)

        outList.append(fileList)

    return outList, secondsLeft


def doPitt(dir, secondsLeft):

    analysisList = list()
    outList = list()
    for file in glob.glob(dir + 'Control/cookie/*.mp3'):
        analysisList.append((file, 'Control', 'Cookie'))
    for file in glob.glob(dir + 'Control/fluency/*.mp3'):
        analysisList.append((file, 'Control', 'Conversation'))
    for file in glob.glob(dir + 'Dementia/cookie/*.mp3'):
        analysisList.append((file, "Alzheimer's", 'Cookie'))
    for file in glob.glob(dir + 'Dementia/fluency/*.mp3'):
        analysisList.append((file, "Alzheimer's", 'Conversation'))
    for file in glob.glob(dir + 'Dementia/recall/*.mp3'):
        analysisList.append((file, "Alzheimer's", 'Recall'))
    for file in glob.glob(dir + 'Dementia/sentence/*.mp3'):
        analysisList.append((file, "Alzheimer's", 'Sentence'))

    for file, diagnosis, task in analysisList:

        fileList = list()
        speaker = os.path.basename(file).split('.')[0]
        tmpSound = AudioSegment.from_mp3(file)
        tmpSound.export('./try.wav', format = 'wav')
        sound = parselmouth.Sound('./try.wav')
        measures = analyzeSound(sound)

        if diagnosis == "Alzheimer's":
            revisedSeconds = send(file, measures[-2], secondsLeft, 1, False, True)
            secondsLeft = revisedSeconds

        else:
            send(file, measures[-2], 1, 1, False, False)

        fileList.append('TalkBank - Pitt')
        fileList.append(diagnosis)
        fileList.append(task)
        fileList.append('MP3')
        fileList.append(speaker)
        fileList.append('True')

        for m in measures:
            fileList.append(m)

        outList.append(fileList)

    return outList, secondsLeft


def doOSU(dir):

    outList = list()
    for file in glob.glob(dir + '*.wav'):

        fileList = list()
        speaker = os.path.basename(file).split('.')[0]
        sound = parselmouth.Sound(file)
        measures = analyzeSound(sound)

        fileList.append('TalkBank - OSU')
        fileList.append("UNK")
        fileList.append("UNK")
        fileList.append('WAV')
        fileList.append(speaker)
        fileList.append('True')

        for m in measures:
            fileList.append(m)

        outList.append(fileList)

    return outList


def doLanzi(dir, secondsLeft):

    analysisList = list()
    outList = list()
    for file in glob.glob(dir + 'Group1/*.mp3'):
        analysisList.append(file)
    for file in glob.glob(dir + 'Group2/*.mp3'):
        analysisList.append(file)

    for file in analysisList:
        fileList = list()

        speaker = os.path.basename(file).split('.')[0]
        tmpSound = AudioSegment.from_mp3(file)
        tmpSound.export('./try.wav', format = 'wav')
        sound = parselmouth.Sound('./try.wav')
        measures = analyzeSound(sound)

        revisedSeconds = send(file, measures[-2], secondsLeft, 1, False, True)
        secondsLeft = revisedSeconds

        fileList.append('TalkBank - Lanzi')
        fileList.append("Alzheimer's")
        fileList.append('Conversation')
        fileList.append('MP3')
        fileList.append(speaker)
        fileList.append('True')
        for m in measures:
            fileList.append(m)

        outList.append(fileList)
        
    return outList, secondsLeft


def doKempler(dir):

    outList = list()
    for file in glob.glob(dir + '0wav/*'):

        fileList = list()
        speaker = os.path.basename(file).split('.')[0]
        sound = parselmouth.Sound(file)
        measures = analyzeSound(sound)

        send(file, measures[-2], 1, 1, True, True)

        fileList.append('TalkBank - Kempler')
        fileList.append("Alzheimer's")
        fileList.append('Conversation')
        fileList.append('WAV')
        fileList.append(speaker)
        fileList.append('True')
        for m in measures:
            fileList.append(m)

        outList.append(fileList)
    return outList


def analyzeTalk2Me(secondsCTRL):

    diagnosedList = [22, 309, 406, 39, 349, 407, 75]
    outList = list()
    for dir in glob.glob('../Talk2Me/*/'):
        if 'picture_description' in dir:
            picList, secondsCTRL  = doPic(dir, 'Picture Description', diagnosedList, secondsCTRL)
            for p in picList:
                outList.append(p)
        if 'sentence_reordering' in dir:
            sentList, secondsCTRL = doPic(dir, 'Sentence Reordering', diagnosedList, secondsCTRL)
            for s in sentList:
                outList.append(s)
        if 'story_recall' in dir:
            storyList, secondsCTRL = doPic(dir, 'Story Recall', diagnosedList, secondsCTRL)
            for s in storyList:
                outList.append(s)
        if 'stroop' in dir:
            stroopList, secondsCTRL = doPic(dir, 'Stroop', diagnosedList, secondsCTRL)
            for s in stroopList:
                outList.append(s)        

    return outList, secondsCTRL


def analyzeTalkBank(secondsLeft):

    outList = list()
    for dir in glob.glob('../TalkBank/*/'):
        if 'Kempler' in dir:
            kemplerList = doKempler(dir)
            for k in kemplerList:
                outList.append(k)
        if 'Lanzi' in dir:
            lanziList, revisedSeconds = doLanzi(dir, secondsLeft)
            secondsLeft = revisedSeconds
            for l in lanziList:
                outList.append(l)
        if 'OSU' in dir:
            osuList = doOSU(dir)
            for o in osuList:
                outList.append(o)
        if 'Pitt' in dir:
            pittList, revisedSeconds = doPitt(dir, secondsLeft)
            secondsLeft = revisedSeconds
            for p in pittList:
                outList.append(p)
        if 'PPA' in dir:
            ppaList, revisedSeconds = doPPA(dir, secondsLeft)
            secondsLeft = revisedSeconds
            for p in ppaList:
                outList.append(p)

    return outList, secondsLeft


def main():

    secondsLeft = 0
    secondsCTRL = 0

    masterList = [['Collection', 'Diagnosis', 'Task', 'Encoding', 'Speaker ID', 'Needs ASR',
                   'Intensity', 'Number of Channels', 'Number of Samples', 'Power', 'Root Mean Squared', 'Sampling Frequency',
                   'Sampling Period', 'Duration', 'Energy']]
    TalkBankList, revisedSeconds = analyzeTalkBank(secondsLeft)
    secondsLeft = revisedSeconds
    print('analyzeTalkBank yields', secondsLeft, "\t That should be around 57k. Is it?")
    for t in TalkBankList:
        masterList.append(t)
    Talk2MeList, secondsCTRL = analyzeTalk2Me(secondsCTRL)
    print('analyzeTalk2Me yields', secondsCTRL, '\t That should be around 57k. is it?')
    for t in Talk2MeList:
        masterList.append(t)

    with open('DementiaData.csv', 'w', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(masterList)


def doubleCheck():

    types = ['Control', 'Diagnosed']
    wavLengths = list()
    for t in types:
        durationMP3, durationWAV = 0.0, 0.0
        for file in glob.glob('../DATA/CHUNKS/{}/*'.format(t)):

            ext = os.path.basename(file).split('.')[-1]
            if ext == 'mp3':
                #continue
                tmpSound = AudioSegment.from_mp3(file)
                tmpSound.export('./try.wav', format = 'wav')
                sound = parselmouth.Sound('./try.wav')
                measures = analyzeSound(sound)
                durationMP3 += float(measures[-2])

            elif ext == 'wav':
                sound = parselmouth.Sound(file)
                measures = analyzeSound(sound)
                durationWAV += float(measures[-2])
                # For finding a file that will be good for creating noise maskers
                if measures[-2] > 250 and measures[-2] < 350:
                    print(file)
            else:
                print(file, 'whoops')
        print(t, '\t', durationMP3, durationWAV)

    print(max(wavLengths))


if __name__ == "__main__":

    #print('Running main()')
    #main()
    print('Running doubleCheck()')
    doubleCheck()

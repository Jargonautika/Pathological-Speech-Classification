#!/usr/bin/env python3

from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent

import parselmouth
import shutil
import glob
import sys
import os


def matchTargetAmplitude(aChunk, target_dBFS):

    change_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_dBFS)


def process(chunks, t, name, ext):

    print(len(chunks), 'chunks in this file.')
    for i, chunk in enumerate(chunks):
        
        # Padding
        silence_chunk = AudioSegment.silent(duration=500)
        audio_chunk = silence_chunk + chunk + silence_chunk
        normalized_chunk = matchTargetAmplitude(audio_chunk, -20.0)
        
        newName = name + '_' + 'chunk' + '_' + str(i) + '.' + ext
        normalized_chunk.export('../DATA/CHUNKS/{0}/{1}'.format(t, newName), format = ext)

def main():

    # Bifurcation
    typeList = ['Control', 'Diagnosed']
    for t in typeList:
        for sound in glob.glob('../DATA/BIG/{}/*'.format(t)):
            path = os.path.basename(sound)
            name = path.split('.')[0]
            ext = path.split('.')[1]
            #print(sound, name, ext)
            if ext == 'wav':
                audio = AudioSegment.from_wav(sound)
            elif ext == 'mp3':
                audio = AudioSegment.from_mp3(sound)
            else:
                print('File {} is neither .wav nor .mp3?'.format(sound))
            
            # Check duration of file
            duration = audio.duration_seconds
            if duration > 6.0:

                #print("{} \t is less than 6.0 seconds.".format(sound))
                # Split the file up wherever you find instances of .5 seconds silence; we consider a chunk silent if it's quieter than -??? dBFS.
                # https://stackoverflow.com/questions/45526996/split-audio-files-using-silence-detection
                #chunks = split_on_silence(audio, min_silence_len = 1000, silence_thresh = -20)
                
                # Just did this once to get everything away from the files that are ok without splitting
                dest = "../DATA/CHUNKS/{0}/{1}".format(t, path)
                shutil.copy(sound, dest)

            else:
                
                dest = "../DATA/CHUNKS/{0}/{1}".format(t, path)
                shutil.move(sound, dest)


if __name__ == "__main__":

    main()

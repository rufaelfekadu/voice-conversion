import glob
import os
import json
import librosa
import soundfile as sf
from tqdm import tqdm
import shutil

data_dir = "/workspace/datasets/Mixat/"
audio_dir = "wav/"

rttm_files = glob.glob(os.path.join(data_dir, "rttm/*.rttm"))
output_path = os.path.join(data_dir, "filtered")
os.makedirs(output_path, exist_ok=True)

def get_consecutive_segments(rttm_file):
    # if consecutive segments have the same speaker, merge them into one segment
    segments = []
    with open(rttm_file, "r") as f:
        for line in f:
            data = line.split()
            speaker = data[-1]
            start = float(data[0])
            end = float(data[1])
            if end-start < 0.05:  # skip segments shorter than 0.5 seconds
                continue
            if len(segments) == 0:
                segments.append((start, end, speaker))
            else:
                last_start, last_end, last_speaker = segments[-1]
                if last_speaker == speaker and start <= last_end:
                    segments[-1] = (last_start, max(last_end, end), last_speaker)
                else:
                    segments.append((start, end, speaker))
    return segments

def split_audio(segments, audio, sr, audio_id):
    for idx, (start, end, speaker) in enumerate(segments):
        duration = end - start
        audio_file = os.path.join(output_path, audio_id, f"{idx:05d}_{speaker}.wav")
        os.makedirs(os.path.join(output_path, audio_id), exist_ok=True)
        sf.write(audio_file, audio[int(start*sr):int(end*sr)], sr)

def filter_audio(rttm_file):
    # if the rttm file containes multiple speakers, discard it
    speakers = set()
    with open(rttm_file, "r") as f:
        for line in f:
            data = line.split()
            speaker = data[-1]
            speakers.add(speaker)
    return len(speakers) == 1

def main():

    for rttm_file in tqdm(rttm_files):
        audio_id = rttm_file.split('/')[-1].split('.')[0]
        audio_file = data_dir + audio_dir + audio_id + ".wav"
        
        segments = get_consecutive_segments(rttm_file)

        # split_audio(segments, audio, sr, audio_id)
        if filter_audio(rttm_file):
            # copy the audio file to the output path
            shutil.copy(audio_file, os.path.join(output_path, audio_id + ".wav"))

            # create a symlink
            


if __name__ == "__main__":
    main()
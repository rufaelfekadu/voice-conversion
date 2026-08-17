import glob
import librosa
import os
import json

def prep_mixat():
    audio_path = "/workspace/datasets/Mixat/wav"
    manifest_path = "/workspace/datasets/Mixat/manifest.json"

    audio_files = glob.glob(os.path.join(audio_path, "TheDirection*.wav"))
    manifest_data_files = []
    for audio_file in audio_files:
        audio_id = os.path.basename(audio_file).split(".")[0]
        duration = librosa.get_duration(filename=audio_file)
        
        # if duration <= 0.5:
        #     print(f"skiping short utterance: {audio_file}")
        #     continue
        
        manifest_data = {
            "audio_filepath": audio_file,
            "duration": duration,
            "offset": 0,
        }
        manifest_data_files.append(manifest_data)

    with open(manifest_path, "w") as f:
        for data in manifest_data_files:
            json.dump(data, f)
            f.write("\n")

def prep_masc():
    pass

if __name__ == '__main__' :
    prep_mixat()

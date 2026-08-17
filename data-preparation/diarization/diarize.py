from nemo.collections.asr.models import SortformerEncLabelModel
import os
import json


diar_model = SortformerEncLabelModel.from_pretrained("nvidia/diar_streaming_sortformer_4spk-v2")
diar_model.eval()

diar_model.sortformer_modules.chunk_len = 340
diar_model.sortformer_modules.chunk_right_context = 40
diar_model.sortformer_modules.fifo_len = 40
diar_model.sortformer_modules.spkcache_update_period = 300

manifest_path = '/workspace/datasets/Mixat/manifest.json'
rttms_path = '/workspace/datasets/Mixat/rttm'
os.makedirs(rttms_path, exist_ok=True)

predicted_segments = diar_model.diarize(audio=manifest_path, batch_size=16)

# load manifest
with open(manifest_path, "r") as f:
    manifest_data = [json.loads(line) for line in f]

# for each audio dump an rttm 
for i, segment in enumerate(predicted_segments):
    audio_id = manifest_data[i]['audio_filepath'].split('/')[-1].split('.')[0]
    rttm_path = f"{rttms_path}/{audio_id}.rttm"
    with open(rttm_path, "w") as f:
        for s in segment:
            f.write(f"{s}\n")
from pathlib import Path
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import torch
import numpy as np
import scipy.io.wavfile as wavfile

def generate_music(description, output_path, index):
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    segment_duration = 10  # in seconds
    sampling_rate = 44100
    tokens_per_second = 20  # estimated
    max_new_tokens = segment_duration * tokens_per_second
    
    inputs = processor(text=description, padding=True, return_tensors="pt").to(device)
    audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=max_new_tokens)
    audio_segment = audio_values[0, 0].cpu().numpy()
    
    repeated_segment = np.tile(audio_segment, 18)  # Repeat the 10-second segment 18 times to make 3 minutes
    
    file_name = f"{description.replace(' ', '_').lower()}_{index}.wav"
    full_path = output_path / file_name
    
    wavfile.write(full_path, rate=sampling_rate, data=repeated_segment)

if __name__ == '__main__':
    description = "Background space music for a game like in a Dune"
    output_path = Path("/home/mikolajnajda/Documents/PySplendor/music_generating/generated_music/")
    output_path.mkdir(parents=True, exist_ok=True)
    
    for i in range(10):
        generate_music(description, output_path, i)

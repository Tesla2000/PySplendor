from pathlib import Path

from transformers import MusicgenForConditionalGeneration, AutoProcessor
import torch
import numpy as np
import scipy.io.wavfile as wavfile

def generate_music(description, output_path):
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    inputs = processor(
        text=description,
        padding=True,
        return_tensors="pt"
    )
    
    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)
    sampling_rate = 44100
        
    file_name = f"{description.replace(' ', '_').lower()}.wav"
    full_path = output_path / file_name
        
    wavfile.write(full_path, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())

if __name__ == '__main__':
    description = "background space music for a game lector"
    
    output_path = Path(".../generated_music")
    generate_music(description, output_path)
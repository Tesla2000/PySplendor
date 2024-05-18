from pathlib import Path

from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile

def generate_speech(texts, output_path):
    model = VitsModel.from_pretrained("facebook/mms-tts-pol")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-pol")

    for i, text in enumerate(texts):
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs).waveform.squeeze()

        output = output.cpu().numpy()

        file_name = f"{'_'.join(text.lower().split())}.wav"
        full_path = output_path / file_name
        
        scipy.io.wavfile.write(full_path, rate=model.config.sampling_rate, data=output)
        print(f"Generated audio saved as {full_path}")

if __name__ == '__main__':
    texts = [
        "Gra rozpoczyna się teraz, przygotuj swoją strategię",
        "Zdobądź jak najwięcej punktów, aby wygrać",
        "Czas na twoją kolej, wykonaj ruch",
        "Gratulacje, osiągnąłeś nowy poziom",
        "Koniec gry, sprawdź swoje wyniki"
    ]
    output_path = Path("../generated_speech")
    generate_speech(texts, output_path)
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np

def mix_audios(speech_file, background_file, output_file, background_volume=0.8):
    """ Mix speech and background audio, adjusting background volume and saving the result. """
    speech_data, speech_rate = librosa.load(speech_file, sr=None)
    background_data, _ = librosa.load(background_file, sr=speech_rate)

    if len(background_data) > len(speech_data):
        background_data = background_data[:len(speech_data)]
    elif len(background_data) < len(speech_data):
        repeat_count = len(speech_data) // len(background_data) + 1
        background_data = np.tile(background_data, repeat_count)[:len(speech_data)]

    background_data *= background_volume

    mixed_data = speech_data + background_data

    mixed_data = np.clip(mixed_data, -1, 1)

    sf.write(output_file, mixed_data, speech_rate, format='WAV')

if __name__ == "__main__":
    speech_file = Path(".../text_to_speech_generating/generated_speech/gra_rozpoczyna_się_teraz,_przygotuj_swoją_strategię.wav")
    background_file = Path(".../music_generating/generated_music/background_space_music_for_a_game_lector.wav")
    output_dir = Path(".../audio_processing/merged_speech_background")

    output_filename = f"{speech_file.stem}_{background_file.stem}.wav"
    output_file = output_dir / output_filename

    mix_audios(speech_file, background_file, output_file)
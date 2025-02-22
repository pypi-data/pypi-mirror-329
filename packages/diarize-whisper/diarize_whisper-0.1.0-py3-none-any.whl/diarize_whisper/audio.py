# diarize_whisper/audio.py
from pydub import AudioSegment
import math

def convert_to_wav_mono(input_file: str, output_file: str = "temp_audio.wav") -> str:
    """
    Convertit un fichier audio en WAV mono 16kHz.
    """
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_file, format="wav")
    return output_file

def split_wav_file(input_file: str, output_prefix: str, segment_length_ms: int = 30*1000) -> None:
    """
    Découpe un fichier WAV en segments d'une durée donnée.
    """
    audio = AudioSegment.from_wav(input_file)
    total_length = len(audio)
    num_segments = math.ceil(total_length / segment_length_ms)

    for i in range(num_segments):
        start = i * segment_length_ms
        end = min((i + 1) * segment_length_ms, total_length)
        segment = audio[start:end]
        output_file = f"{output_prefix}_part_{i+1}.wav"
        segment.export(output_file, format="wav")
        print(f"Segment {i+1} exporté vers {output_file}")

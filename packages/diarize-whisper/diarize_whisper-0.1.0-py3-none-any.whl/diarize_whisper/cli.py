# diarize_whisper/cli.py
import os
import argparse
from diarize_whisper.audio import convert_to_wav_mono, split_wav_file
from diarize_whisper.asr import get_device, get_torch_dtype, load_asr_pipeline
from diarize_whisper.diarization import load_diarization_pipeline
from diarize_whisper.transcript import (
    combine_transcript_diarization,
    refine_segments_with_context,
    reconstruct_dialogues,
)

def main():
    parser = argparse.ArgumentParser(description="Pipeline ASR et Diarisation")
    parser.add_argument("--input", type=str, required=True, help="Chemin vers le fichier audio d'entrée")
    parser.add_argument("--output", type=str, default="resultats_dialogues.txt", help="Fichier de sortie pour les dialogues")
    parser.add_argument("--chunk_duration", type=int, default=25, help="Durée des chunks en secondes")
    parser.add_argument("--asr_model", type=str, default="openai/whisper-large-v3-turbo", help="Modèle ASR à utiliser")
    parser.add_argument("--diarization_model", type=str, default="pyannote/speaker-diarization-3.1", help="Modèle de diarisation à utiliser")
    parser.add_argument("--token", type=str, required=True, help="Token d'authentification HuggingFace")
    parser.add_argument('--num_speakers', type=int, required=False, help="Nombre de speakers")
    parser.add_argument('--min_speakers', type=int, help="Nombre de speakers minumum")
    parser.add_argument("--max_speakers", type=int, help="Nombre de speakers maximum")
    args = parser.parse_args()

    device = get_device()
    torch_dtype = get_torch_dtype()

    asr_pipeline = load_asr_pipeline(args.asr_model, args.token, device, torch_dtype, chunk_length_s=args.chunk_duration)
    diarization_pipeline = load_diarization_pipeline(args.diarization_model, device="cuda")

    # Conversion et découpage du fichier audio
    wav_file = convert_to_wav_mono(args.input, "sample.wav")
    split_dir = "output_chunks"
    os.makedirs(split_dir, exist_ok=True)
    split_wav_file(wav_file, os.path.join(split_dir, "audio"), segment_length_ms=args.chunk_duration * 1000)

    # Diarisation globale sur le fichier complet
    dia_result = diarization_pipeline(wav_file, num_speakers=args.num_speakers, min_speakers=args.min_speakers, max_speakers=args.max_speakers)

    all_merged_segments = []
    files = sorted(os.listdir(split_dir))  # Assurer l'ordre correct

    for idx, file in enumerate(files):
        file_path = os.path.join(split_dir, file)
        try:
            transcript_result = asr_pipeline(file_path, return_timestamps="word")
        except TypeError as e:
            if "'<=' not supported" in str(e):
                print(f"Erreur détectée pour {file}: {e}. Relance de la pipeline avec return_timestamps=True")
                transcript_result = asr_pipeline(file_path, return_timestamps=True)
            else:
                raise e

        # Ajustement des timestamps selon l'offset du chunk
        offset = idx * args.chunk_duration
        for chunk in transcript_result.get("chunks", []):
            start, end = chunk["timestamp"]
            if start is not None and end is not None:
                chunk["timestamp"] = (start + offset, end + offset)

        merged_segments = combine_transcript_diarization(dia_result, transcript_result)
        all_merged_segments.extend(merged_segments)
        all_merged_segments = refine_segments_with_context(all_merged_segments, tolerance=0.2)

    dialogues = reconstruct_dialogues(all_merged_segments)
    with open(args.output, "w", encoding="utf-8") as f:
        for dialogue in dialogues:
            line = f"[{dialogue['speaker']} ({dialogue['start']} - {dialogue['end']})] {dialogue['text']}\n"
            print(line)
            f.write(line)

if __name__ == "__main__":
    main()

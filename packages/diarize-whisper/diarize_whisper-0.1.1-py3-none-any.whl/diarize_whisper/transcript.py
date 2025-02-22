# diarize_whisper/transcript.py

def combine_transcript_diarization(diarization, transcript, default_time: float = 0.0):
    """
    Combine les informations de transcription et de diarisation.
    """
    merged_segments = []
    diarization_segments = list(diarization.itertracks(yield_label=True))
    chunks = transcript.get("chunks", [])
    speakers = [None] * len(chunks)

    for i, chunk in enumerate(chunks):
        text_start, text_end = chunk.get("timestamp", (None, None))
        if text_start is not None and text_end is not None:
            for turn, _, speaker in diarization_segments:
                if turn.start <= text_start and turn.end >= text_end:
                    speakers[i] = speaker
                    break

    for i, chunk in enumerate(chunks):
        text_start, text_end = chunk.get("timestamp", (None, None))
        if text_start is None:
            if i > 0 and chunks[i-1].get("timestamp", (None, None))[1] is not None:
                text_start = chunks[i-1]["timestamp"][1]
            else:
                for j in range(i+1, len(chunks)):
                    ns, _ = chunks[j].get("timestamp", (None, None))
                    if ns is not None:
                        text_start = ns
                        break
                if text_start is None:
                    text_start = default_time
        if text_end is None:
            if i < len(chunks)-1 and chunks[i+1].get("timestamp", (None, None))[0] is not None:
                text_end = chunks[i+1]["timestamp"][0]
            else:
                text_end = text_start

        assigned_speaker = speakers[i]
        if assigned_speaker is None:
            if i > 0 and speakers[i-1] is not None:
                assigned_speaker = speakers[i-1]
            else:
                for j in range(i+1, len(chunks)):
                    if speakers[j] is not None:
                        assigned_speaker = speakers[j]
                        break
        if assigned_speaker is None:
            assigned_speaker = "UNKNOWN"

        merged_segments.append({
            "speaker": assigned_speaker,
            "start": round(text_start, 2),
            "end": round(text_end, 2),
            "text": chunk["text"]
        })

    return merged_segments

def refine_segments_with_context(segments, tolerance: float = 0.2):
    """
    Ajuste les segments en fonction du contexte (segments précédent et suivant).
    """
    refined = segments.copy()
    for i, seg in enumerate(refined):
        if i > 0:
            prev_seg = refined[i-1]
            if seg["start"] - prev_seg["end"] <= tolerance:
                if seg["text"].strip().startswith("-") or seg["text"].strip()[0] in {",", ".", ";", ":"}:
                    seg["speaker"] = prev_seg["speaker"]
        if i > 0 and i < len(refined)-1:
            prev_seg = refined[i-1]
            next_seg = refined[i+1]
            if len(seg["text"].split()) < 3 and prev_seg["speaker"] == next_seg["speaker"]:
                seg["speaker"] = prev_seg["speaker"]
    return refined

def reconstruct_dialogues(segments):
    """
    Reconstruit des dialogues en regroupant les segments continus du même locuteur.
    """
    dialogues = []
    if not segments:
        return dialogues

    current_speaker = segments[0]['speaker']
    current_start = segments[0]['start']
    current_end = segments[0]['end']
    current_text = [segments[0]['text']]

    for seg in segments[1:]:
        speaker = seg['speaker']
        if speaker != current_speaker:
            dialogues.append({
                'speaker': current_speaker,
                'start': current_start,
                'end': current_end,
                'text': " ".join(current_text)
            })
            current_speaker = speaker
            current_start = seg['start']
            current_text = [seg['text']]
        else:
            current_text.append(seg['text'])
        current_end = seg['end']

    dialogues.append({
        'speaker': current_speaker,
        'start': current_start,
        'end': current_end,
        'text': " ".join(current_text)
    })
    return dialogues

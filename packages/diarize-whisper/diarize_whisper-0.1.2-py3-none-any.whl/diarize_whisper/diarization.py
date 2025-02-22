# diarize_whisper/diarization.py
import torch
from pyannote.audio import Pipeline

def load_diarization_pipeline(model_id: str, device: str = "cuda"):
    """
    Charge et retourne une pipeline de diarisation.
    
    Args:
        model_id: Identifiant du modèle de diarisation.
        device: Device à utiliser (par défaut "cuda").
    
    Returns:
        Pipeline de diarisation.
    """
    diarization = Pipeline.from_pretrained(model_id)
    return diarization.to(torch.device(device))

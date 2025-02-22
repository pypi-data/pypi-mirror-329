# diarize_whisper/asr.py
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def get_device() -> str:
    """
    Retourne le device ('cuda:0' ou 'cpu') selon la disponibilité.
    """
    return "cuda:0" if torch.cuda.is_available() else "cpu"

def get_torch_dtype() -> torch.dtype:
    """
    Retourne le type de tenseur adapté (float16 si CUDA est disponible).
    """
    return torch.float16 if torch.cuda.is_available() else torch.float32

def load_asr_pipeline(
    model_id: str,
    token: str,
    device: str,
    torch_dtype: torch.dtype,
    batch_size: int = 16,
    chunk_length_s: int = 25
):
    """
    Charge et retourne une pipeline ASR configurée.
    
    Args:
        model_id: Identifiant du modèle ASR.
        token: Token d'authentification HuggingFace.
        device: Device à utiliser.
        torch_dtype: Type de tenseur.
        batch_size: Taille de batch.
        chunk_length_s: Durée des segments en secondes.
    
    Returns:
        Pipeline de transcription automatique.
    """
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
        token=token
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id, token=token)
    asr_pipeline_instance = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        batch_size=batch_size,
        chunk_length_s=chunk_length_s,
        torch_dtype=torch_dtype,
        device=device,
    )
    return asr_pipeline_instance

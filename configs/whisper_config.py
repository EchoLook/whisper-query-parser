"""
Configuration for Whisper models.
"""
from typing import Dict, List

# Model sizes and their approximate memory requirements
MODEL_SIZES = {
    "tiny": {"params": "39M", "english_only": False, "multilingual": True, "required_vram": "~1 GB"},
    "base": {"params": "74M", "english_only": False, "multilingual": True, "required_vram": "~1 GB"},
    "small": {"params": "244M", "english_only": False, "multilingual": True, "required_vram": "~2 GB"},
    "medium": {"params": "769M", "english_only": False, "multilingual": True, "required_vram": "~5 GB"},
    "large": {"params": "1550M", "english_only": False, "multilingual": True, "required_vram": "~10 GB"},
    # English-only models (smaller and faster for English)
    "tiny.en": {"params": "39M", "english_only": True, "multilingual": False, "required_vram": "~1 GB"},
    "base.en": {"params": "74M", "english_only": True, "multilingual": False, "required_vram": "~1 GB"},
    "small.en": {"params": "244M", "english_only": True, "multilingual": False, "required_vram": "~2 GB"},
    "medium.en": {"params": "769M", "english_only": True, "multilingual": False, "required_vram": "~5 GB"},
}

# Default transcription options
DEFAULT_OPTIONS = {
    "fp16": True,  # Use half-precision float16 for faster inference
    "language": None,  # Auto-detect language by default
    "task": "transcribe",  # Default task is transcription (not translation)
    "temperature": 0,  # Sampling temperature (0 = greedy decoding)
    "best_of": 5,  # Number of samples to consider for beam decoding
    "beam_size": 5,  # Beam size for beam search
    "patience": 1.0,  # Hyperparameter for beam search
    "length_penalty": 1.0,  # Hyperparameter for beam search length normalization
    "suppress_tokens": "-1",  # Tokens to suppress during generation
    "initial_prompt": None,  # Optional text to provide as initial prompt for the first window
    "condition_on_previous_text": True,  # Whether to condition on previous text for real-time
    "compression_ratio_threshold": 2.4,  # Threshold for filtering out stretches of audio
    "log_prob_threshold": -1.0,  # Threshold for filtering out unlikely transcriptions
    "no_speech_threshold": 0.6,  # Threshold for detecting no speech
}

# Supported languages with their ISO codes
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "hi": "Hindi",
    "ko": "Korean",
    "tr": "Turkish",
    "pl": "Polish",
    # Additional languages supported by Whisper
    "ca": "Catalan",
    "cs": "Czech",
    "da": "Danish",
    "el": "Greek",
    "fi": "Finnish",
    "he": "Hebrew",
    "hu": "Hungarian",
    "id": "Indonesian",
    "no": "Norwegian",
    "ro": "Romanian",
    "sv": "Swedish",
    "th": "Thai",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
}

def get_model_info(model_name: str) -> Dict:
    """
    Get information about a specific model.
    
    Args:
        model_name (str): Name of the model.
    
    Returns:
        Dict: Model information.
    """
    if model_name not in MODEL_SIZES:
        raise ValueError(f"Model {model_name} not found. Available models: {list(MODEL_SIZES.keys())}")
    
    return MODEL_SIZES[model_name]


def get_available_models(english_only: bool = False) -> List[str]:
    """
    Get list of available models.
    
    Args:
        english_only (bool): Whether to return only English models.
    
    Returns:
        List[str]: List of available model names.
    """
    if english_only:
        return [m for m, info in MODEL_SIZES.items() if info["english_only"]]
    
    return list(MODEL_SIZES.keys()) 
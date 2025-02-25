from typing import Dict, List

class AIConfig:
    """Configuration for AI services."""

    TYPE_TEXT_GENERATION = "text_generation"

    # Available models for each service
    AVAILABLE_MODELS = {
        TYPE_TEXT_GENERATION : ["gpt-3.5", "gpt-4", "chat_glm"],
        "image_generation": ["stable-diffusion", "dall-e"],
        "image_understanding": ["vision-1", "vision-2"],
        "video_generation": ["gen-1"],
        "video_understanding": ["perceive-1"],
        "audio_recognition": ["whisper"],
        "audio_synthesis": ["tts-1"],
        "ocr": ["ocr-1"]
    }

    @classmethod
    def get_available_models(cls, service_type: str) -> List[str]:
        """Get available models for a specific service type."""
        return cls.AVAILABLE_MODELS.get(service_type, []) 
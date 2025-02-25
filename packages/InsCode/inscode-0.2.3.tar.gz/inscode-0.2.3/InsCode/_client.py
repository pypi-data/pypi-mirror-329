import os
import openai
from .ai import Chat, Images, Audio, OCR
from .common import DEFAULT_BASE_URL

__all__ = ["InsCode"]


class InsCode:
    chat: Chat
    images: Images
    audio: Audio
    ocr: OCR

    def __init__(self,
                 *,
                 api_key: str | None = None,
                 base_url: str | None = None):
        self.api_key = api_key
        if self.api_key is None:
            self.api_key = os.environ.get("INSCODE_API_KEY")
        self.base_url = base_url

        if base_url is None:
            self.base_url = os.environ.get("INSCODE_BASE_URL")

        if base_url is None:
            self.base_url = DEFAULT_BASE_URL
        if not self.api_key:
            raise ValueError(
                "API key is required. Please provide it through the api_key parameter or set the INSCODE_API_KEY environment variable.")

        if not self.base_url:
            raise ValueError(
                "Base URL is required. Please provide it through the base_url parameter or set the INSCODE_BASE_URL environment variable.")

        self.openai_client = openai.OpenAI(api_key=self.api_key,
                                           base_url=self.base_url)
        self.chat = self.openai_client.chat
        self.images = self.openai_client.images
        self.audio = self.openai_client.audio
        self.ocr = OCR(api_key=self.api_key, base_url=self.base_url)

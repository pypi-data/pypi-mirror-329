import json

from ...core import BaseAIService

__all__ = ['OCR']

from typing import Dict, Any, Optional


class OCR(BaseAIService):

    def __init__(self, api_key: str,
                 base_url: Optional[str] = None):
        super().__init__(api_key, base_url)

    def recognize(self,
                  image: bytes | str,
                  model: str = "default_ocr",
                  type: str = "Advanced",
                  params: str | Dict[str, Any] = "{}",
                  **kwargs) -> Dict[str, Any]:

        if isinstance(params, str):
            try:
                params = eval(params)  # Convert string to dict
            except:
                params = {}
        elif params is None:
            params = {}

        payload = {
            "model": model,
            "type": type,
            "params": json.dumps(params),
            **kwargs
        }

        return self._process_post_form(payload, files={"image":image})

    def api_url(self) -> str:
        return "images/ocr"

import requests

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..common import DEFAULT_BASE_URL


class BaseAIService(ABC):
    def __init__(self, api_key: str,
                 base_url: Optional[str] = DEFAULT_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def _process_get(self, payload: Dict[str, Any]) -> Any:
        """Process GET request"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url or ''}/{self.api_url()}"
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def _process_post_form(self, payload: Dict[str, Any], files: Dict[str, Any] = None) -> Any:
        """Process POST request with form data"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        url = f"{self.base_url or ''}/{self.api_url()}"

        processed_files = {}
        data = {}

        if files:
            for key, file_path in files.items():
                if isinstance(file_path, bytes):
                    processed_files[key] = file_path
                elif isinstance(file_path, str):
                    if file_path.startswith(('http://', 'https://')):
                        try:
                            response = requests.get(file_path)
                            if response.status_code != 200:
                                raise ValueError(f"Failed to download file from URL: {file_path}, status code: {response.status_code}")
                            processed_files[key] = response.content
                        except Exception as e:
                            raise ValueError(f"Failed to download file from URL: {file_path}, error: {str(e)}")
                    else:
                        try:
                            with open(file_path, 'rb') as f:
                                processed_files[key] = f.read()
                        except FileNotFoundError:
                            raise ValueError(f"File not found: {file_path}")
                        except Exception as e:
                            raise ValueError(f"Failed to read file: {file_path}, error: {str(e)}")
                else:
                    raise ValueError(f"File must be either bytes or a string path/URL for key: {key}")

        # Process regular payload data
        for key, value in payload.items():
            if isinstance(value, bytes):
                processed_files[key] = value
            else:
                data[key] = value

        response = requests.post(url, data=data, files=processed_files, headers=headers)
        response.raise_for_status()
        return response.json()

    def _process_post_json(self, payload: Dict[str, Any]) -> Any:
        """Process POST request with JSON data"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url or ''}/{self.api_url()}"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def api_url(self) -> str:
        pass

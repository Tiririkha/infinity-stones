from typing import Any, Dict, Optional, List
import logging
import requests
from .config import TimestoneConfig
from .exceptions import (
    TimestoneAuthError,
    TimestoneAPIError,
    TimestoneConnectionError,
    TimestoneNotFoundError
)

logger = logging.getLogger(__name__)

class TimestoneClient:
    def __init__(
            self,
            timeout: Optional[int] = None,
    ):
        config_params = {}
        if timeout:
            config_params["timeout"] = timeout

        self.config = TimestoneConfig(**config_params)
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @classmethod
    def _handle_response(cls, response: requests.Response) -> Any:
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise TimestoneAuthError("Invalid API key")
            elif response.status_code == 404:
                raise TimestoneNotFoundError("Resource not found")
            else:
                raise TimestoneAPIError(f"API error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TimestoneConnectionError(f"Connection error: {str(e)}")

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            data: Optional[Dict] = None,
            json: Optional[Dict] | List[Dict] = None
    ) -> Any:
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                params=params,
                data=data,
                json=json,
                timeout=self.config.timeout,
            )
            return self._handle_response(response)
        except Exception as e:
            raise TimestoneConnectionError(f"Request failed: {str(e)}")
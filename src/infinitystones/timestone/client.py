from typing import Optional, Dict, Union, List, Any, TypeVar
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from json.decoder import JSONDecodeError
from contextlib import contextmanager

from infinitystones.config import settings
from infinitystones.timestone.config import TimestoneConfig
from infinitystones.timestone.exceptions import *

logger = logging.getLogger(__name__)

T = TypeVar('T')


class TimestoneClient:
    """Base HTTP client for Timestone API with improved error handling and session management"""

    def __init__(
            self,
            timeout: Optional[int] = None,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            max_retries: Optional[int] = None
    ):
        self.config = TimestoneConfig(
            timeout=timeout or settings.TIMEOUT,
            api_key=api_key or settings.API_KEY,
            base_url=base_url or settings.BASE_URL,
            max_retries=max_retries or settings.MAX_RETRIES
        )
        self._session = None
        logger.debug(f"Initialized TimestoneClient with base_url={self.config.base_url}")

    @property
    def session(self) -> requests.Session:
        """Lazy session initialization"""
        if self._session is None:
            self._session = self._create_session()
        return self._session

    def _create_session(self) -> requests.Session:
        """Create session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.retry_backoff,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=frozenset(["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]),
            raise_on_redirect=True,
            raise_on_status=True
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=self.config.pool_connections,
            pool_maxsize=self.config.pool_maxsize,
            pool_block=True
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with error handling"""
        if not self.config.api_key:
            raise TimestoneAuthError("API key not configured")

        return {
            "Authorization": f"{self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def _handle_response(response: requests.Response) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Enhanced response handler with detailed error processing"""
        if not response.content:
            return {}

        try:
            data = response.json()
        except JSONDecodeError as e:
            raise TimestoneAPIError(
                f"Invalid JSON response: {str(e)}",
                status_code=response.status_code,
                response=response
            )

        if response.status_code >= 400:
            error_data = data.get('error', {})
            error_msg = error_data.get('message', str(error_data) if error_data else 'error')
            error_details = error_data.get('details', {})

            error_mapping = {
                400: (TimestoneBadRequestError, "Bad Request"),
                401: (TimestoneAuthError, "Authentication failed"),
                403: (TimestoneForbiddenError, "Forbidden"),
                404: (TimestoneNotFoundError, "Resource not found"),
                405: (TimestoneMethodNotAllowedError, "Method not allowed"),
                406: (TimestoneNotAcceptableError, "Not acceptable"),
                408: (TimestoneRequestTimeoutError, "Request timeout"),
                409: (TimestoneConflictError, "Conflict"),
                410: (TimestoneGoneError, "Resource gone"),
                411: (TimestoneLengthRequiredError, "Length required"),
                412: (TimestonePreconditionFailedError, "Precondition failed"),
                413: (TimestonePayloadTooLargeError, "Payload too large"),
                414: (TimestoneURITooLongError, "URI too long"),
                415: (TimestoneUnsupportedMediaTypeError, "Unsupported media type"),
                416: (TimestoneRangeNotSatisfiableError, "Range not satisfiable"),
                417: (TimestoneExpectationFailedError, "Expectation failed"),
                422: (TimestoneValidationError, "Validation failed"),
                429: (TimestoneRateLimitError, "Rate limit exceeded"),
                431: (TimestoneRequestHeaderFieldsTooLargeError, "Header fields too large"),
                451: (TimestoneUnavailableForLegalReasonsError, "Unavailable for legal reasons")
            }

            error_class, prefix = error_mapping.get(
                response.status_code,
                (TimestoneAPIError, f"API error ({response.status_code})")
            )

            detailed_msg = f"{error_msg}. Details: {error_details}" if error_details else error_msg
            raise error_class(
                f"{prefix}: {detailed_msg}",
                status_code=response.status_code,
                response=response
            )

        return data

    @contextmanager
    def _request_context(self, method: str, url: str, timeout: int):
        """Context manager for request error handling"""
        try:
            yield
        except requests.exceptions.Timeout:
            raise TimestoneConnectionError(f"Request timed out after {timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise TimestoneConnectionError(f"Connection failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TimestoneConnectionError(str(e))
        except Exception as e:
            raise TimestoneAPIError(str(e))

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
            **kwargs
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Enhanced request method with improved error handling"""
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        timeout = kwargs.pop('timeout', self.config.timeout)

        with self._request_context(method, url, timeout):
            logger.debug(f"Making {method} request to {url}")
            response = self.session.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                params=params,
                json=json,
                timeout=timeout,
                **kwargs
            )
            return self._handle_response(response)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Union[
        Dict[str, Any], List[Dict[str, Any]]]:
        """Make GET request with improved error handling"""
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Union[
        Dict[str, Any], List[Dict[str, Any]]]:
        """Make POST request with improved error handling"""
        return self._request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Union[
        Dict[str, Any], List[Dict[str, Any]]]:
        """Make PUT request with improved error handling"""
        return self._request("PUT", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make DELETE request with improved error handling"""
        return self._request("DELETE", endpoint, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close session and cleanup resources"""
        if self._session:
            self._session.close()
            self._session = None

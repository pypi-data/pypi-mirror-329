import requests
import base64
import urllib.parse
import json
from functools import wraps
from typing import Optional, Dict, Any, List


class CxReportClientV1:
    """
    A client for interacting with the CxReport API.

    This class provides methods for fetching reports, pushing temporary data, and managing authentication tokens.

    Attributes:
        base_url (str): The base URL for the API.
        workspace_id (int): The workspace ID for the API context.
        token (str): The authentication token used for API requests.
    """
    def __init__(self, base_url:str, default_workspace_id:int, token:str):
        self.url = base_url
        self.token = token
        self.workspace_id = default_workspace_id

    def __get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
        }
    
    def __get_url_with_workspace(self, url:str, workspace_id:int = None):
        return f"{self.url}/api/v1/ws/{self.workspace_id if workspace_id == None else workspace_id}/{url}"
    
    def __get_preview_url(self, url:str, workspace_id:int = None):
        return f"{self.url}/ws/{self.workspace_id if workspace_id == None else workspace_id}/{url}"
    
    def __handle_requests_exceptions(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as http_err:
                raise RuntimeError(f"HTTP error occurred: {http_err}") from http_err
            except requests.exceptions.ConnectionError as conn_err:
                raise RuntimeError(f"Connection error occurred: {conn_err}") from conn_err
            except requests.exceptions.Timeout as timeout_err:
                raise RuntimeError(f"Timeout occurred: {timeout_err}") from timeout_err
            except requests.exceptions.RequestException as req_err:
                raise RuntimeError(f"An error occurred: {req_err}") from req_err
        return wrapper

    @__handle_requests_exceptions
    def get_pdf(self, reportId: int, params: dict = None, workspace_id:int = None):
        """
        Fetch a PDF report.

        Args:
            report_id (int): The ID of the report.
            query_params (Optional[Dict[str, Any]]): Optional query parameters for the request.

        Returns:
            bytes: The PDF content.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        headers = self.__get_headers()
        url = self.__get_url_with_workspace(f"reports/{reportId}/pdf", workspace_id)

        url = self.__append_query_params(url, params)
        print(url)

        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        if "application/pdf" not in response.headers.get("Content-Type", "").lower():
            raise RuntimeError("Invalid content type, expected PDF")

        return response.content

    @__handle_requests_exceptions
    def get_report_types(self, workspace_id:int = None):
        headers = self.__get_headers()
        url = self.__get_url_with_workspace("report-types", workspace_id)

        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

            # Check if the response content is HTML
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        return response.json()

    @__handle_requests_exceptions
    def get_workspaces(self):
        """
        Fetch the list of available workspaces.

        Returns:
            List[Dict[str, Any]]: A list of workspaces.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        headers = self.__get_headers()
        url = f"{self.url}/api/v1/workspaces"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

            # Check if the response content is HTML
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        return response.json()
            
    @__handle_requests_exceptions
    def get_reports(self, type: str, workspace_id:int = None):
        """
        Fetch the list of reports by type.

        Args:
            report_type (str): The type of report to fetch.

        Returns:
            List[Dict[str, Any]]: A list of reports.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        headers = self.__get_headers()
        url = self.__get_url_with_workspace(f"reports?type={type}", workspace_id)
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        # Check if the response content is HTML
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        return response.json()

    @__handle_requests_exceptions
    def create_auth_token(self):
        """
        Create a new authentication token.

        Returns:
            Dict[str, Any]: The new authentication token details.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        headers = self.__get_headers()
        url = f"{self.url}/api/v1/nonce-tokens"
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()

        # Check if the response content is HTML
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        return response.json()

    @__handle_requests_exceptions
    def push_temporary_data(self, data:dict):
        """
        Push temporary data to the API.

        Args:
            data (Dict[str, Any]): The data to be pushed.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        headers = self.__get_headers()

        url = self.__get_url_with_workspace("temporary-data")
        data = {
            "content": data
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        
        # If content type is HTML, then the user is not authenticated
        if response.headers.get('Content-Type', '').lower().startswith('text/html'):
            raise RuntimeError("Unauthenticated.")

        return response.json()
    
    def get_preview_url(self, report_id:int, query_params:dict = None, workspace_id:int = None):
        """
        Get the preview URL for a report.

        Args:
            report_id (int): The ID of the report.
            query_params (Optional[Dict[str, Any]]): Optional query parameters for the request.

        Returns:
            str: The preview URL.

        Raises:
            RuntimeError: If any request or processing error occurs.
        """
        url = self.__get_preview_url(f"reports/{report_id}/preview", workspace_id)
        nonce_token = self.create_auth_token()['nonce']
        query_params = query_params or {}
        query_params['nonce'] = nonce_token
        url = self.__append_query_params(url, query_params)
        return url
    
    
    
    def __append_query_params(self, url: str, query_params: Dict[str, Any]) -> str:
        """
        Append query parameters to the URL.

        Args:
            url (str): The base URL.
            query_params (Dict[str, Any]): The query parameters to append.

        Returns:
            str: The URL with query parameters attached.
        """
        
        if query_params is None:
            return url
        params = {}

        if 'tempDataId' in query_params and isinstance(query_params['tempDataId'], int):
            params['tempDataId'] = query_params['tempDataId']

        if 'params' in query_params and isinstance(query_params['params'], dict):
            json_params = json.dumps(query_params['params'])
            encoded_params = base64.urlsafe_b64encode(json_params.encode()).decode()
            params['params'] = encoded_params
            
        if 'nonce' in query_params and isinstance(query_params['nonce'], str):
            params['nonce'] = query_params['nonce']
            
        if 'data' in query_params and isinstance(query_params['data'], str):
            params['data'] = query_params['data']
            
        if 'timezone' in query_params and isinstance(query_params['timezone'], str):
            params['timezone'] = query_params['timezone']

        return f"{url}?{urllib.parse.urlencode(params)}"
    
    

# client.py
from typing import Optional, Dict, Any, List
from datetime import datetime
import requests
from .models import Event, DecodingResult
from .exceptions import StegawaveError, AuthenticationError
import os

class StegawaveClient:
    def __init__(self, api_key: str, base_url: str = "https://api.stegawave.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def _get_headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            del kwargs["headers"]

        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    raise StegawaveError(error_data.get('error', str(e)))
                except:
                    pass
            raise StegawaveError(str(e))

    def list_events(self, active: Optional[bool] = None) -> List[Event]:
        """List all events."""
        params = {"active": str(active).lower()} if active is not None else None
        response = self._request("GET", "/events", params=params)
        return [Event.model_validate(event) for event in response.get("events", [])]

    def create_event(self, name: str, start_time: datetime, end_time: datetime, 
                    ip_whitelist: Optional[List[str]] = None) -> Event:
        """Create a new event."""
        data = {
            "eventName": name,
            "startTime": start_time.isoformat(),
            "endTime": end_time.isoformat(),
            "ipWhitelist": ip_whitelist or []
        }
        response = self._request("POST", "/create-event", json=data)
        return Event.model_validate(response)


    def decode_file(self, event_id: str, file_path: str) -> Dict[str, Any]:
        """Decode a file using multipart upload."""
        # Step 1: Initiate upload
        initiate_data = {
            "eventID": event_id,
            "filename": os.path.basename(file_path),
            "fileType": "application/octet-stream"  # Default type
        }
        initiate_response = self._request("POST", "/upload/initiate", json=initiate_data)
        upload_id = initiate_response["uploadId"]
        key = initiate_response["key"]

        # Step 2: Get presigned URL
        presigned_url_data = {
            "uploadId": upload_id,
            "key": key,
            "partNumber": 1  
        }
        
        presigned_url_response = self._request("POST", "/upload/presigned-url", json=presigned_url_data)
        presigned_url = presigned_url_response["presignedUrl"]

        # Step 3: Upload file
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.put(presigned_url, files=files)
            response.raise_for_status()
            etag = response.headers.get('ETag', '').strip('"')

        # Step 4: Complete upload
        complete_data = {
            "uploadId": upload_id,
            "key": key,
            "eventID": event_id,
            "parts": [{"ETag": etag, "PartNumber": 1}]
        }
        complete_response = self._request("POST", "/upload/complete", json=complete_data)
        return complete_response
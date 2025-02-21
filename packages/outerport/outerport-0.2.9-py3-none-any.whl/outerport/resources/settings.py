from __future__ import annotations
from typing import Any, Dict
import requests
from outerport.resources.base_resource import BaseResource


class SettingsResource(BaseResource):
    def update(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user settings.
        """
        url = f"{self.client.base_url}/api/v0/settings"
        headers = self.client._json_headers()
        payload = {"settings_data": settings_data}
        resp = requests.put(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()

    def retrieve(self) -> Dict[str, Any]:
        """
        Get user settings.
        """
        url = f"{self.client.base_url}/api/v0/settings"
        headers = self.client._json_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

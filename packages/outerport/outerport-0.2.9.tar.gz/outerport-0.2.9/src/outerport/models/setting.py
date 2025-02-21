from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel, PrivateAttr
from datetime import datetime

if TYPE_CHECKING:
    from outerport.client import OuterportClient


class Setting(BaseModel):
    """
    A Pydantic model that represents User Settings in your API.
    """

    id: int
    user_id: int
    language: str = "en"
    created_at: datetime
    updated_at: datetime

    # Private attribute to store the client
    _client: OuterportClient = PrivateAttr()

    def __init__(self, **data):
        """
        Pydantic's __init__ is overridden so we can attach _client after the model is constructed.
        """
        client = data.pop("_client", None)
        super().__init__(**data)
        self._client = client

    def save(self) -> None:
        """
        Save the current settings to the server.
        """
        result = self._client.settings.update(self.settings_data)
        # Update current model with any returned data
        self.settings_data = result.get("settings_data", self.settings_data)

    def reload(self) -> None:
        """
        Refresh this Setting with the latest data from the server.
        """
        fresh = self._client.settings.retrieve()
        self.settings_data = fresh.get("settings_data", {})

    @classmethod
    def from_api(cls, data: dict, client) -> Setting:
        """
        Helper to create a Setting from an API response dict plus the client reference.
        """
        return cls(_client=client, **data)

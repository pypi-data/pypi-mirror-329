from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, PrivateAttr
from datetime import datetime

if TYPE_CHECKING:
    from outerport.client import OuterportClient


class RetentionPolicy(BaseModel):
    """
    A Pydantic model that represents a Retention Policy in your API.
    """

    id: int
    name: str
    description: Optional[str] = None
    duration_days: int
    delete_after_expiry: bool = False
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
        Save the current retention policy to the server.
        """
        if hasattr(self, "id"):
            # Update existing policy
            result = self._client.retention_policies.update(
                self.id,
                {
                    "name": self.name,
                    "description": self.description,
                    "duration_days": self.duration_days,
                    "delete_after_expiry": self.delete_after_expiry,
                },
            )
        else:
            # Create new policy
            result = self._client.retention_policies.create(
                {
                    "name": self.name,
                    "description": self.description,
                    "duration_days": self.duration_days,
                    "delete_after_expiry": self.delete_after_expiry,
                }
            )

        # Update current model with returned data
        for key, value in result.model_dump().items():
            setattr(self, key, value)

    def reload(self) -> None:
        """
        Refresh this RetentionPolicy with the latest data from the server.
        """
        if not hasattr(self, "id"):
            raise ValueError("Cannot reload a retention policy without an ID")

        fresh = self._client.retention_policies.retrieve(self.id)
        for key, value in fresh.model_dump().items():
            setattr(self, key, value)

    def delete(self) -> None:
        """
        Delete this retention policy from the server.
        """
        if not hasattr(self, "id"):
            raise ValueError("Cannot delete a retention policy without an ID")

        self._client.retention_policies.delete(self.id)

    @classmethod
    def from_api(cls, data: dict, client) -> RetentionPolicy:
        """
        Helper to create a RetentionPolicy from an API response dict plus the client reference.
        """
        return cls(_client=client, **data)

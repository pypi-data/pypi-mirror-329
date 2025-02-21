# outerport/models/document_model.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING, IO, List
from pydantic import BaseModel, PrivateAttr
from datetime import datetime
from .retention_policy import RetentionPolicy

if TYPE_CHECKING:
    from outerport.client import OuterportClient


class Document(BaseModel):
    """
    A Pydantic model that represents a Document in your API.
    """

    id: int
    name: str
    folder_id: Optional[int] = None
    file_path: Optional[str] = None
    file_type: str
    file_url: Optional[str] = None
    summary: str
    version: int
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

    def delete(self) -> dict:
        """
        Delete this document on the server.
        """
        return self._client.documents.delete(self.id)

    def reload(self) -> None:
        """
        Refresh this Document with the latest data from the server.
        """
        fresh = self._client.documents.retrieve(self.id)
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    def update_metadata(
        self,
        name: Optional[str] = None,
        folder_id: Optional[int] = None,
        summary: Optional[str] = None,
    ) -> None:
        """
        Update this document's metadata on the server and refresh the local instance.

        :param name: Optional new name for the document
        :param folder_id: Optional new folder ID for the document
        :param summary: Optional new summary for the document
        """
        fresh = self._client.documents.update_metadata(
            self.id,
            name=name,
            folder_id=folder_id,
            summary=summary,
        )
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    def update_file(self, file: IO[bytes], file_name: Optional[str] = None) -> None:
        """
        Update this document's file content on the server and refresh the local instance.

        :param file: The new file content to upload
        :param file_name: Optional name for the file
        """
        fresh = self._client.documents.update_file(self.id, file, file_name)
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    @classmethod
    def from_api(cls, data: dict, client):
        """
        Helper to create a Document from an API response dict plus the client reference.
        """
        # The API might return 'id' or 'document_id'. Adjust as needed.
        if "document_id" in data and "id" not in data:
            data["id"] = data.pop("document_id")
        return cls(_client=client, **data)

    @property
    def tags(self) -> List[str]:
        """
        Get all tags associated with this document.

        :return: A list of tag names.
        """
        return self._client.documents.get_tags(self.id)

    def add_tags(self, tags: List[str]) -> None:
        """
        Add tags to this document and refresh the local instance.

        :param tags: List of tag names to add to the document.
        """
        fresh = self._client.documents.add_tags(self.id, tags)
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    def remove_tags(self, tags: List[str]) -> None:
        """
        Remove tags from this document and refresh the local instance.

        :param tags: List of tag names to remove from the document.
        """
        fresh = self._client.documents.remove_tags(self.id, tags)
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    @property
    def retention_policies(self) -> List[RetentionPolicy]:
        """
        Get the retention policies associated with this document.
        """
        return self._client.documents.get_retention_policies(self.id)

    def add_retention_policy(self, retention_policy: RetentionPolicy) -> None:
        """
        Add a retention policy to this document and refresh the local instance.

        :param retention_policy: The retention policy to add to the document.
        """
        fresh = self._client.documents.add_retention_policy_by_id(
            self.id, retention_policy.id
        )
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    def remove_retention_policy(self, retention_policy: RetentionPolicy) -> None:
        """
        Remove the retention policy from this document and refresh the local instance.
        """
        fresh = self._client.documents.remove_retention_policy_by_id(
            self.id, retention_policy.id
        )
        # Update current model in-place
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

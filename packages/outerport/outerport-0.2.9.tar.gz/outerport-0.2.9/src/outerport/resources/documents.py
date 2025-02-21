# outerport/resources/documents.py
from typing import IO, List, Optional, Dict, Any
import requests
from outerport.models.document import Document
from outerport.resources.base_resource import BaseResource
from outerport.models.retention_policy import RetentionPolicy


class DocumentsResource(BaseResource):
    def create(self, file: IO[bytes], file_name: Optional[str] = None) -> Document:
        """
        Upload a document and wait synchronously for it to finish processing.
        Returns a fully-populated Document object.

        :param file: The file to upload.
        :param file_name: The name of the file to upload.
        :return: The uploaded Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents"
        headers = self.client._form_headers()

        if not file_name:
            file_name = getattr(file, "name", "uploaded_file")

        files = {"file": (file_name, file, "application/octet-stream")}
        resp = requests.post(url, headers=headers, files=files)
        resp.raise_for_status()

        data = resp.json()  # e.g. { "job_status_id": 1, "document_id": "123", ... }
        job_status_id = data.get("job_status_id")
        document_id = data.get("document_id")
        if not job_status_id or not document_id:
            raise ValueError("Upload response missing job_status_id or document_id.")

        # Wait for job to complete
        self.client.job_statuses.wait_for_completion(job_status_id)

        # Now retrieve the final Document from the server
        return self.retrieve(document_id)

    def list(
        self,
        folder_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        tag: Optional[str] = None,
    ) -> List[Document]:
        """
        List all documents as a list of Document objects.

        :param folder_id: The ID of the folder to filter documents by.
        :param owner_id: The ID of the owner to filter documents by.
        :param tag: The name of the tag to filter documents by.
        :return: A list of Document objects.
        """
        url = f"{self.client.base_url}/api/v0/documents"
        headers = self.client._json_headers()
        params = {}
        if folder_id:
            params["folder_id"] = folder_id
        if tag:
            params["tag_name"] = tag
        if owner_id:
            params["owner_id"] = owner_id
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        raw_list = resp.json()  # e.g. [ { "id": 1, ... }, { ... } ]

        return [Document.from_api(d, self.client) for d in raw_list]

    def retrieve(self, document_id: int) -> Document:
        """
        Retrieve a single Document by ID.

        :param document_id: The ID of the document to retrieve.
        :return: The Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}"
        headers = self.client._json_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return Document.from_api(data, self.client)

    def delete(self, document_id: int) -> dict:
        """
        Delete the document from the server.

        :param document_id: The ID of the document to delete.
        :return: A dictionary containing the response from the server.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}"
        headers = self.client._json_headers()
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def update_metadata(
        self,
        document_id: int,
        name: Optional[str] = None,
        folder_id: Optional[int] = None,
        summary: Optional[str] = None,
    ) -> Document:
        """
        Update a document's metadata.

        :param document_id: The ID of the document to update.
        :param name: Optional new name for the document.
        :param folder_id: Optional new folder ID for the document.
        :param summary: Optional new summary for the document.
        :return: The updated Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}"
        headers = self.client._json_headers()

        # Only include non-None values in the payload
        payload = {}
        payload["name"] = name
        payload["folder_id"] = folder_id
        payload["summary"] = summary

        resp = requests.put(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return Document.from_api(data, self.client)

    def update_file(
        self, document_id: int, file: IO[bytes], file_name: Optional[str] = None
    ) -> Document:
        """
        Update a document's file content and wait for processing to complete.

        :param document_id: The ID of the document to update.
        :param file: The new file content to upload.
        :param file_name: Optional name for the file.
        :return: The updated Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}/file"
        headers = self.client._form_headers()

        if not file_name:
            file_name = getattr(file, "name", "updated_file")

        files = {"file": (file_name, file, "application/octet-stream")}
        resp = requests.put(url, headers=headers, files=files)
        resp.raise_for_status()

        data = resp.json()
        job_status_id = data.get("job_status_id")
        if not job_status_id:
            raise ValueError("Update response missing job_status_id.")

        # Wait for job to complete
        self.client.job_statuses.wait_for_completion(job_status_id)

        # Now retrieve the final Document from the server
        return self.retrieve(document_id)

    def get_tags(self, document_id: int) -> List[str]:
        """
        Get all tags for a document.

        :param document_id: The ID of the document to get tags for.
        :return: A list of tag names.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}/tags"
        headers = self.client._json_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return []
        return [tag["name"] for tag in data]

    def add_tags(self, document_id: int, tags: List[str]) -> Document:
        """
        Add tags to a document.

        :param document_id: The ID of the document to tag.
        :param tags: List of tag names to add to the document.
        :return: The updated Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}/tags"
        headers = self.client._json_headers()
        payload = {"tag_names": tags}

        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return Document.from_api(data, self.client)

    def remove_tags(self, document_id: int, tags: List[str]) -> Document:
        """
        Remove tags from a document.

        :param document_id: The ID of the document to remove tags from.
        :param tags: List of tag names to remove from the document.
        :return: The updated Document object.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}/tags"
        headers = self.client._json_headers()
        payload = {"tag_names": tags}

        resp = requests.delete(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return Document.from_api(data, self.client)

    def search(
        self,
        query: str,
        folder_id: Optional[int] = None,
        tag: Optional[str] = None,
        owner_id: Optional[int] = None,
    ) -> List[Document]:
        """
        Search for documents based on the provided query and filters.

        :param query: The search query string.
        :param folder_id: Optional folder ID to filter documents by.
        :param tag: Optional tag name to filter documents by.
        :param owner_id: Optional owner ID to filter documents by.
        :return: List of Document objects.
        """
        url = f"{self.client.base_url}/api/v0/documents/search"
        headers = self.client._json_headers()

        payload: Dict[str, Any] = {
            "query": query,
            "folder_id": folder_id,
            "tag_name": tag,
            "owner_id": owner_id,
        }

        # Initiate search
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        search_id = data.get("search_id")
        job_status_id = data.get("job_status_id")

        if not search_id:
            raise ValueError("Search response missing search_id")

        # Wait for search job to complete if there is one
        if job_status_id:
            self.client.job_statuses.wait_for_completion(job_status_id)

        # Get final results
        url = f"{self.client.base_url}/api/v0/documents/search/{search_id}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        documents = data["documents"]
        return [Document.from_api(d, self.client) for d in documents]

    def get_retention_policies(self, document_id: int) -> List[RetentionPolicy]:
        """
        Get all retention policies for a document.

        :param document_id: The ID of the document to get retention policies for.
        :return: A list of RetentionPolicy objects.
        """
        url = (
            f"{self.client.base_url}/api/v0/documents/{document_id}/retention-policies"
        )
        headers = self.client._json_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return [RetentionPolicy.from_api(d, self.client) for d in data]

    def add_retention_policy_by_id(
        self, document_id: int, retention_policy_id: int
    ) -> Document:
        """
        Add a retention policy to a document.

        :param document_id: The ID of the document to add the retention policy to.
        :param retention_policy_id: The ID of the retention policy to add to the document.
        """
        url = (
            f"{self.client.base_url}/api/v0/documents/{document_id}/retention-policies"
        )
        headers = self.client._json_headers()
        params = {"retention_policy_id": retention_policy_id}
        resp = requests.post(url, headers=headers, params=params)
        resp.raise_for_status()
        # Reload the document to get the latest state
        return self.retrieve(document_id)

    def remove_retention_policy_by_id(
        self, document_id: int, retention_policy_id: int
    ) -> Document:
        """
        Remove the retention policy from a document.

        :param document_id: The ID of the document to remove the retention policy from.
        """
        url = f"{self.client.base_url}/api/v0/documents/{document_id}/retention-policies/{retention_policy_id}"
        headers = self.client._json_headers()
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        # Reload the document to get the latest state
        return self.retrieve(document_id)

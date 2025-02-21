from typing import Optional

from .resources.documents import DocumentsResource
from .resources.questions import QuestionsResource
from .resources.settings import SettingsResource
from .resources.job_statuses import JobStatusesResource
from .resources.retention_policies import RetentionPoliciesResource


class OuterportClient:
    """
    Outerport API client.
    It exposes each resource class as a property.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: str = "http://localhost:8080"
    ) -> None:
        """
        :param api_key: API key or bearer token for Authorization.
        :param base_url: Base URL of the Outerport API.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

        # Resource namespaces
        self.documents = DocumentsResource(self)
        self.questions = QuestionsResource(self)
        self.settings = SettingsResource(self)
        self.job_statuses = JobStatusesResource(self)
        self.retention_policies = RetentionPoliciesResource(self)

    def _json_headers(self) -> dict:
        """
        Return standard JSON headers. Adds Authorization if api_key is set.
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _form_headers(self) -> dict:
        """
        Return headers for multipart/form-data (file uploads).
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

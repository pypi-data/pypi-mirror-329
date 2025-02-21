from typing import List, Optional, Dict, Any
import requests
from outerport.models.retention_policy import RetentionPolicy
from outerport.resources.base_resource import BaseResource


class RetentionPoliciesResource(BaseResource):
    def create(
        self,
        name: str,
        description: Optional[str] = None,
        duration_days: int = 7,
        delete_after_expiry: bool = True,
    ) -> RetentionPolicy:
        """
        Create a new retention policy.

        Args:
            name: str
            description: Optional[str]
            duration_days: int
            delete_after_expiry: bool

        Returns:
            RetentionPolicy: The created retention policy
        """
        # Check if the retention policy already exists
        existing_policy = self.retrieve_by_name(name)
        if existing_policy:
            return existing_policy

        url = f"{self.client.base_url}/api/v0/retention-policies"
        headers = self.client._json_headers()
        payload = {
            "name": name,
            "description": description,
            "duration_days": duration_days,
            "delete_after_expiry": delete_after_expiry,
        }
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return RetentionPolicy.from_api(resp.json(), self.client)

    def list(self) -> List[RetentionPolicy]:
        """
        List all retention policies.

        Returns:
            List[RetentionPolicy]: List of retention policies
        """
        url = f"{self.client.base_url}/api/v0/retention-policies"
        headers = self.client._json_headers()

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return [RetentionPolicy.from_api(d, self.client) for d in resp.json()]

    def retrieve(self, policy_id: int) -> RetentionPolicy:
        """
        Retrieve a single retention policy by ID.

        Args:
            policy_id: The ID of the retention policy to retrieve

        Returns:
            RetentionPolicy: The requested retention policy
        """
        url = f"{self.client.base_url}/api/v0/retention-policies/{policy_id}"
        headers = self.client._json_headers()

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return RetentionPolicy.from_api(resp.json(), self.client)

    def update(self, policy_id: int, data: Dict[str, Any]) -> RetentionPolicy:
        """
        Update an existing retention policy.

        Args:
            policy_id: The ID of the retention policy to update
            data: Dictionary containing the fields to update:
                - name: Optional[str]
                - description: Optional[str]
                - duration_days: Optional[int]
                - delete_after_expiry: Optional[bool]

        Returns:
            RetentionPolicy: The updated retention policy
        """
        url = f"{self.client.base_url}/api/v0/retention-policies/{policy_id}"
        headers = self.client._json_headers()

        resp = requests.put(url, headers=headers, json=data)
        resp.raise_for_status()
        return RetentionPolicy.from_api(resp.json(), self.client)

    def delete(self, policy_id: int) -> RetentionPolicy:
        """
        Delete a retention policy.

        Args:
            policy_id: The ID of the retention policy to delete

        Returns:
            RetentionPolicy: The deleted retention policy
        """
        url = f"{self.client.base_url}/api/v0/retention-policies/{policy_id}"
        headers = self.client._json_headers()

        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return RetentionPolicy.from_api(resp.json(), self.client)

    def retrieve_by_name(self, name: str) -> Optional[RetentionPolicy]:
        """
        Retrieve a single retention policy by name.

        Args:
            name: The name of the retention policy to retrieve

        Returns:
            Optional[RetentionPolicy]: The requested retention policy, or None if not found
        """
        policies = self.list()
        for policy in policies:
            if policy.name == name:
                return policy
        return None

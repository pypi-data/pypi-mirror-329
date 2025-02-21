# outerport/resources/questions.py
from typing import List
import requests
from outerport.models.question import Question
from outerport.resources.base_resource import BaseResource
from outerport.models.document import Document


class QuestionsResource(BaseResource):
    def create(
        self,
        documents: List[Document],
        question: str,
        chunk_type: str = "32000_char_chunk",
        llm_provider: str = "openai",
        answer_mode: str = "reasoning",
    ) -> Question:
        """
        Ask a question referencing some documents, wait for job completion, return a final Question object.
        """
        url = f"{self.client.base_url}/api/v0/questions"
        headers = self.client._json_headers()

        payload = {
            "document_ids": [d.id for d in documents],
            "chunk_type": chunk_type,
            "question": question,
            "llm_provider": llm_provider,
            "answer_mode": answer_mode,
        }

        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()  # e.g. { "question_id": 123, "job_status_id": 45, ... }

        question_id = data.get("question_id")
        job_status_id = data.get("job_status_id")
        if question_id is None:
            raise ValueError("No question_id returned from create().")

        # If there's a job status, poll until done
        if job_status_id:
            self.client.job_statuses.wait_for_completion(job_status_id)

        # Retrieve the final question object
        return self.retrieve(question_id)

    def retrieve(self, question_id: int) -> Question:
        url = f"{self.client.base_url}/api/v0/questions/{question_id}"
        headers = self.client._json_headers()
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return Question.from_api(data, self.client)

    def delete(self, question_id: int) -> dict:
        url = f"{self.client.base_url}/api/v0/questions/{question_id}"
        headers = self.client._json_headers()
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

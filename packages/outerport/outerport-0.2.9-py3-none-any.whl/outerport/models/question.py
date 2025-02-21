# outerport/models/question_model.py
from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, PrivateAttr
from datetime import datetime

if TYPE_CHECKING:
    from outerport.client import OuterportClient


class Evidence(BaseModel):
    id: int
    evidence: str
    reasoning: str
    document_id: int
    sequence_number: int


class Question(BaseModel):
    id: int
    user_id: int
    question_text: str
    plan: Optional[str] = None
    evidences: List[Evidence] = []
    final_answer: Optional[str] = None
    answer_mode: str
    llm_provider: str
    chunk_type: str
    job_status_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    _client: OuterportClient = PrivateAttr()

    def __init__(self, **data):
        client = data.pop("_client", None)
        super().__init__(**data)
        self._client = client

    def reload(self) -> None:
        fresh = self._client.questions.retrieve(self.id)
        for field_name, value in fresh.model_dump().items():
            if field_name != "_client":
                setattr(self, field_name, value)

    def delete(self) -> dict:
        return self._client.questions.delete(self.id)

    @classmethod
    def from_api(cls, data: dict, client):
        return cls(_client=client, _evidences=[], **data)

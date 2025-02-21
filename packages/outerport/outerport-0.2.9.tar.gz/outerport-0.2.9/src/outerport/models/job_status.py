# outerport/models/job_status_model.py
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class JobStatus(BaseModel):
    id: int
    user_id: int
    status: str  # e.g. "queued", "processing", "done", "error"
    error_message: Optional[str] = None
    created_at: str

    def is_done(self) -> bool:
        return self.status == "done"

    def is_error(self) -> bool:
        return self.status == "error"

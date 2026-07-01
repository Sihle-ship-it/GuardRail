from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4, UUID

from app.domain.submission_status import SubmissionStatus


@dataclass
class CodeSubmission:
    code: str
    language: str
    id: UUID = field(default_factory=uuid4)
    status: SubmissionStatus = SubmissionStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_reason: str | None = None

    def start_analysis(self):
        if self.status != SubmissionStatus.PENDING:
            raise ValueError("Cannot start analysis. Submission is not in PENDING status.")

        self.status = SubmissionStatus.ANALYZING
        self.updated_at = datetime.now(timezone.utc)
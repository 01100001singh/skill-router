"""Audit trail logging for compliance."""

import json
import logging
from datetime import datetime
from pathlib import Path

from skill_router.core.types import DispatchResult


class AuditLogger:
    """
    Audit logger for skill routing decisions.

    Provides immutable, timestamped logs of all routing decisions
    for regulatory compliance and debugging.
    """

    def __init__(
        self,
        log_path: Path | str | None = None,
        log_level: int = logging.INFO
    ):
        """
        Initialize audit logger.

        Args:
            log_path: Path to audit log file
            log_level: Logging level
        """
        self.log_path = Path(log_path) if log_path else None
        self.logger = logging.getLogger("skill_router.audit")
        self.logger.setLevel(log_level)

        if self.log_path:
            handler = logging.FileHandler(self.log_path)
            handler.setFormatter(
                logging.Formatter("%(message)s")
            )
            self.logger.addHandler(handler)

    def log_dispatch(
        self,
        result: DispatchResult,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict | None = None
    ) -> dict:
        """
        Log a dispatch decision.

        Args:
            result: Dispatch result to log
            user_id: Optional user identifier
            session_id: Optional session identifier
            metadata: Optional additional metadata

        Returns:
            The logged audit record
        """
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "skill_dispatch",
            "skill_name": result.skill_name,
            "confidence": result.confidence,
            "strategy": result.routing_strategy,
            "alternatives": [
                {"skill": name, "score": score}
                for name, score in result.alternatives
            ],
            "audit_trail": result.audit_trail,
            "user_id": user_id,
            "session_id": session_id,
            "metadata": metadata or {}
        }

        self.logger.info(json.dumps(record))
        return record

    def query_logs(
        self,
        skill_name: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None
    ) -> list[dict]:
        """
        Query audit logs.

        Args:
            skill_name: Filter by skill name
            start_time: Filter by start time
            end_time: Filter by end time

        Returns:
            List of matching audit records
        """
        if not self.log_path or not self.log_path.exists():
            return []

        records = []
        with open(self.log_path) as f:
            for line in f:
                try:
                    record = json.loads(line)

                    if skill_name and record.get("skill_name") != skill_name:
                        continue

                    record_time = datetime.fromisoformat(record["timestamp"])

                    if start_time and record_time < start_time:
                        continue

                    if end_time and record_time > end_time:
                        continue

                    records.append(record)
                except (json.JSONDecodeError, KeyError):
                    continue

        return records
